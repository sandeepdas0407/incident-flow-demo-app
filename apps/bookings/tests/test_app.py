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


def test_booking_ids_renumbered_in_same_order_with_details_unchanged():
    from app import BOOKINGS

    assert BOOKINGS == [
        {"id": 101, "room": "Everest", "owner": "Fabrikam", "date": "2026-12-01"},
        {"id": 102, "room": "Kilimanjaro", "owner": "Northwind", "date": "2026-12-03"},
        {"id": 103, "room": "Denali", "owner": "Tailspin", "date": "04/12/2026"},
    ]


def test_index_shows_renumbered_booking_ids():
    html = client().get("/").get_data(as_text=True)
    tbody = html.split("<tbody>", 1)[1].split("</tbody>", 1)[0]
    for new_id in (101, 102, 103):
        assert f"<td>{new_id}</td>" in tbody
    for old_id in (501, 502, 503):
        assert f"<td>{old_id}</td>" not in tbody
    assert tbody.index("<td>101</td>") < tbody.index("<td>102</td>") < tbody.index("<td>103</td>")


def test_api_bookings_ok_with_renumbered_ids_in_order():
    resp = client().get("/api/bookings")
    assert resp.status_code == 200
    bookings = resp.get_json()["bookings"]
    assert [b["id"] for b in bookings] == [101, 102, 103]
    assert [(b["room"], b["owner"], b["date"]) for b in bookings] == [
        ("Everest", "Fabrikam", "2026-12-01"),
        ("Kilimanjaro", "Northwind", "2026-12-03"),
        ("Denali", "Tailspin", "04/12/2026"),
    ]


def test_with_weekday_parses_legacy_date_as_day_month_year():
    from app import with_weekday

    out = with_weekday([{"id": 103, "date": "04/12/2026"}])
    assert out[0]["weekday"] == "Friday"


def test_with_weekday_skips_unparseable_date():
    from app import with_weekday

    out = with_weekday([{"id": 1, "date": "not a date"}])
    assert out == [{"id": 1, "date": "not a date"}]
