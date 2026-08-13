#!/usr/bin/env python3
"""
Offline end-to-end harness for the skill's Step 7 (run on the VPS).

Executes list_events.py / create_event.py logic against a mock Calendar
service that mimics googleapiclient.discovery.build("calendar", "v3") —
same calls, same parameters, same response shapes — so the scripts can be
validated here without network access to the real Google API.

Run:  python3 run_demo.py
"""
import json
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

# ---------------------------------------------------------------- mock service
class MockEvent:
    def __init__(self, summary, start, end, timezone="America/Sao_Paulo"):
        self.summary = summary
        self.start = start
        self.end = end
        self.timezone = timezone
        self.id = "evt_" + summary.lower().replace(" ", "_")[:24]
        self.htmlLink = (
            "https://www.google.com/calendar/event?eid=" + self.id
        )


def _iso_local(hour, minute=0, day_offset=0):
    dt = datetime.now(timezone.utc) + timedelta(days=day_offset)
    return dt.replace(hour=hour, minute=minute, second=0, microsecond=0).isoformat()


class MockCalendar:
    """Backing store that only keeps events within the next 7 days."""

    def __init__(self):
        self.events = [
            MockEvent("Squad sync", _iso_local(9, 0, 0), _iso_local(9, 30, 0)),
            MockEvent("1:1 com estagiaria", _iso_local(14, 0, 0), _iso_local(14, 45, 0)),
            MockEvent("Plantao NAPJe", _iso_local(8, 0, 0, 1), _iso_local(12, 0, 0, 1)),
            MockEvent("Reuniao de planejamento", _iso_local(10, 0, 0, 2), _iso_local(11, 30, 0, 2)),
        ]

    def list(self, **params):
        time_min = params["timeMin"]
        time_max = params["timeMax"]
        items = [
            {
                "id": e.id,
                "summary": e.summary,
                "start": {"dateTime": e.start, "timeZone": e.timezone},
                "end": {"dateTime": e.end, "timeZone": e.timezone},
            }
            for e in self.events
            if time_min <= e.start <= time_max
        ]
        if params.get("orderBy") == "startTime":
            items.sort(key=lambda ev: ev["start"]["dateTime"])
        return type("Resp", (), {"execute": lambda: {"items": items}})()

    def insert(self, calendarId=None, body=None):
        ev = MockEvent(body["summary"], body["start"]["dateTime"], body["end"]["dateTime"])
        self.events.append(ev)
        return type("Resp", (), {"execute": lambda: {
            "id": ev.id, "summary": ev.summary, "htmlLink": ev.htmlLink,
            "start": body["start"], "end": body["end"],
        }})()


def build(service_name, version, credentials=None):
    assert service_name == "calendar" and version == "v3"
    assert credentials is not None, "no credentials passed to build()"
    return type("Service", (), {"events": lambda: MockCalendar()})()


# ------------------------------------------------------------- script code paths
from gcal_service import TOKEN_PATH
from list_events import main as list_main
from create_event import main as create_main

if __name__ == "__main__":
    print("== Step 7a: events().list() — upcoming events (next 7 days) ==")
    with patch("gcal_service.build", side_effect=build):
        list_main()

    print()
    print("== Step 7b: events().insert() — create a new event ==")
    with patch("gcal_service.build", side_effect=build):
        import sys
        sys.argv = [
            "create_event.py",
            "Publicacao no Diario do Gestor",
            "2026-08-14T09:00:00",
            "2026-08-14T09:15:00",
            "Revisar e publicar a edicao diaria",
        ]
        create_main()

    print()
    print("== Re-list after insert (should include the new event) ==")
    with patch("gcal_service.build", side_effect=build):
        list_main()
