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


def test_index_shows_total_bookings_under_heading():
    from app import BOOKINGS

    html = client().get("/").get_data(as_text=True)
    line = f"Total bookings: {len(BOOKINGS)}"
    assert line in html
    after_heading = html.split("</h1>", 1)[1].lstrip()
    assert after_heading.startswith(f'<p class="total">{line}</p>')
    tbody = html.split("<tbody>", 1)[1].split("</tbody>", 1)[0]
    assert tbody.count("<tr>") == len(BOOKINGS)
