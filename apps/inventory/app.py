"""Contoso Inventory - warehouse stock levels and low-stock alerts.

Pilot app (2 of 3) managed by the Incident Flow AI Ops agents. Served on port 8081.
"""
from flask import Flask, jsonify, render_template

app = Flask(__name__)

ITEMS = [
    {"sku": "WID-100", "name": "Widget", "qty": 140, "reorder_level": 50},
    {"sku": "GAD-220", "name": "Gadget", "qty": 12, "reorder_level": 25},
    {"sku": "SPR-310", "name": "Sprocket", "qty": 8},  # added by the new supplier feed
]


def low_stock(items):
    """SKUs whose quantity is below their reorder level."""
    return [i["sku"] for i in items if i["qty"] < i["reorder_level"]]


@app.route("/")
def index():
    return render_template("index.html", items=ITEMS)


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/api/stock")
def api_stock():
    return jsonify(items=ITEMS, low_stock=low_stock(ITEMS))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=False)
