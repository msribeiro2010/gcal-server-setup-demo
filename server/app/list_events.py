#!/usr/bin/env python3
"""List Google Calendar events for the next 7 days (read via events().list())."""
from datetime import datetime, timedelta, timezone

from gcal_service import get_calendar_service


def main():
    service = get_calendar_service()
    now = datetime.now(timezone.utc)
    time_max = now + timedelta(days=7)

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now.isoformat(),
            timeMax=time_max.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    print(f"Events between {now.isoformat()} and {time_max.isoformat()}:")
    if not events:
        print("  (none)")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))
        print(f"  {start} -> {end}  {event.get('summary', '(no title)')}")


if __name__ == "__main__":
    main()
