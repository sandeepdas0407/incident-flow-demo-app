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


def test_api_stock_handles_missing_reorder_level():
    resp = client().get("/api/stock")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "GAD-220" in data["low_stock"]
    assert "WID-100" not in data["low_stock"]
    assert "SPR-310" not in data["low_stock"]
