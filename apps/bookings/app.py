"""Contoso Bookings - meeting room reservations.

Pilot app (3 of 3) managed by the Incident Flow AI Ops agents. Served on port 8082.
"""
from datetime import datetime

from flask import Flask, jsonify, render_template

app = Flask(__name__)

BOOKINGS = [
    {"id": 501, "room": "Everest", "owner": "Fabrikam", "date": "2026-12-01"},
    {"id": 502, "room": "Kilimanjaro", "owner": "Northwind", "date": "2026-12-03"},
    {"id": 503, "room": "Denali", "owner": "Tailspin", "date": "04/12/2026"},  # imported from the legacy system
]


def with_weekday(bookings):
    """Add the weekday name to each booking for the calendar view."""
    out = []
    for b in bookings:
        day = datetime.strptime(b["date"], "%Y-%m-%d")
        out.append({**b, "weekday": day.strftime("%A")})
    return out


@app.route("/")
def index():
    return render_template("index.html", bookings=BOOKINGS)


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/api/bookings")
def api_bookings():
    return jsonify(bookings=with_weekday(BOOKINGS))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=False)
