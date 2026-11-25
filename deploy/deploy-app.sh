#!/bin/bash
# Deploys all three pilot apps on the VM (idempotent).
# Run by app-deploy.yml through `az vm run-command` (as root, without $HOME), and by cloud-init on first boot.
set -euo pipefail
export HOME=/root
REPO=/opt/app
GIT="git -c safe.directory=$REPO -C $REPO"
$GIT fetch --depth 1 origin main
$GIT reset --hard origin/main

# name:internal_port:public_port
APPS="orders:8000:80 inventory:8001:8081 bookings:8002:8082"

# Retire the single-app layout from before the pilot (app/ + contoso-orders.service).
if [ -f /etc/systemd/system/contoso-orders.service ]; then
  systemctl disable --now contoso-orders >/dev/null 2>&1 || true
  rm -f /etc/systemd/system/contoso-orders.service
fi
rm -f /etc/nginx/sites-enabled/default

for entry in $APPS; do
  IFS=: read -r name port public <<< "$entry"
  /opt/venv/bin/pip install -q -r "$REPO/apps/$name/requirements.txt"
  default=""
  [ "$public" = "80" ] && default=" default_server"
  cat > "/etc/systemd/system/pilot-$name.service" <<EOF
[Unit]
Description=Pilot app $name (gunicorn)
After=network.target

[Service]
WorkingDirectory=$REPO/apps/$name
ExecStart=/opt/venv/bin/gunicorn --workers 2 --bind 127.0.0.1:$port app:app
Restart=always
User=www-data

[Install]
WantedBy=multi-user.target
EOF
  cat > "/etc/nginx/sites-available/pilot-$name" <<EOF
server {
  listen $public$default;
  location / {
    proxy_pass http://127.0.0.1:$port;
    proxy_set_header Host \$host;
  }
}
EOF
  ln -sf "/etc/nginx/sites-available/pilot-$name" "/etc/nginx/sites-enabled/pilot-$name"
done

systemctl daemon-reload
for entry in $APPS; do
  name=${entry%%:*}
  systemctl enable "pilot-$name" >/dev/null 2>&1
  systemctl restart "pilot-$name"
done
nginx -t -q
systemctl reload nginx

# Health-check each app from inside the VM (the NSG may not expose the new ports yet).
for entry in $APPS; do
  IFS=: read -r name port public <<< "$entry"
  curl -fsS --retry 10 --retry-delay 2 --retry-connrefused -o /dev/null "http://127.0.0.1:$public/health" \
    || { echo "health check failed: $name"; exit 1; }
done
echo "deployed $($GIT rev-parse --short HEAD)"
