#!/bin/bash
# Runs on the VM as root via `az vm run-command` (sent inline by .github/workflows/app-deploy.yml).
# run-command does not set $HOME, so avoid anything that needs it (e.g. `git config --global`).
set -euo pipefail
export HOME=/root
GIT="git -c safe.directory=/opt/app -C /opt/app"
$GIT fetch --depth 1 origin main
$GIT reset --hard origin/main
/opt/venv/bin/pip install -q -r /opt/app/app/requirements.txt
systemctl restart contoso-orders
echo "deployed $($GIT rev-parse --short HEAD)"
