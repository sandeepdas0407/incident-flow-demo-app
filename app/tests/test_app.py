import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import app  # noqa: E402


def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_index_ok():
    assert client().get("/").status_code == 200


def test_health_ok():
    assert client().get("/health").get_json() == {"status": "ok"}


def test_api_orders_ok_with_no_shipped_orders():
    resp = client().get("/api/orders")
    assert resp.status_code == 200
    assert resp.get_json()["stats"]["avg_shipped"] == 0.0


def test_compute_order_stats_handles_empty_and_shipped():
    from app import compute_order_stats

    assert compute_order_stats([]) == {"count": 0, "total": 0, "avg_shipped": 0.0}
    stats = compute_order_stats([
        {"id": 1, "customer": "A", "amount": 10.0, "status": "shipped"},
        {"id": 2, "customer": "B", "amount": 20.0, "status": "shipped"},
        {"id": 3, "customer": "C", "amount": 5.0, "status": "pending"},
    ])
    assert stats == {"count": 3, "total": 35.0, "avg_shipped": 15.0}
