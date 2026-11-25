"""Contoso Orders - a tiny demo app deployed on an Azure VM.

It intentionally contains a seeded bug in /api/orders (see compute_order_stats)
so the Incident Flow agent has something real to diagnose and fix.
"""
from flask import Flask, jsonify, render_template

app = Flask(__name__)

ORDERS = [
    {"id": 1001, "customer": "Fabrikam", "amount": 120.50, "status": "pending"},
    {"id": 1002, "customer": "Northwind", "amount": 75.00, "status": "pending"},
    {"id": 1003, "customer": "Tailspin", "amount": 310.25, "status": "processing"},
]


def compute_order_stats(orders):
    shipped = [o for o in orders if o["status"] == "shipped"]
    total = sum(o["amount"] for o in orders)
    # BUG: when no orders have shipped yet this divides by zero -> HTTP 500
    avg_shipped = sum(o["amount"] for o in shipped) / len(shipped) if shipped else 0.0
    return {"count": len(orders), "total": round(total, 2), "avg_shipped": round(avg_shipped, 2)}


@app.route("/")
def index():
    return render_template("index.html", orders=ORDERS)


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/api/orders")
def api_orders():
    return jsonify(orders=ORDERS, stats=compute_order_stats(ORDERS))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
