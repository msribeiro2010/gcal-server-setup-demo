#!/usr/bin/env python3
"""Create a Google Calendar event via events().insert().

Usage: create_event.py <summary> <start_iso> <end_iso> [description]
"""
import sys

from gcal_service import get_calendar_service


def main():
    if len(sys.argv) < 4:
        print("Usage: create_event.py <summary> <start_iso> <end_iso> [description]")
        sys.exit(1)

    summary, start_iso, end_iso = sys.argv[1], sys.argv[2], sys.argv[3]
    description = sys.argv[4] if len(sys.argv) > 4 else ""

    service = get_calendar_service()
    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_iso, "timeZone": "America/Sao_Paulo"},
        "end": {"dateTime": end_iso, "timeZone": "America/Sao_Paulo"},
    }

    created = service.events().insert(calendarId="primary", body=event).execute()
    print(f"Created event: {created.get('htmlLink')}")
    print(f"  id: {created.get('id')}")


if __name__ == "__main__":
    main()
