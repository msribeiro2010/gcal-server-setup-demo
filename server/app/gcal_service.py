#!/usr/bin/env python3
"""
Loads Google Calendar OAuth credentials from the transferred token file
(/app/data/google_calendar_token.json) and builds an authenticated
Calendar API service using google-auth + google-api-python-client.

Usage:
    from gcal_service import get_calendar_service
    service = get_calendar_service()
"""
import json

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = "/app/data/google_calendar_token.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():
    """Load credentials from the transferred token file and build the service."""
    with open(TOKEN_PATH, "r") as f:
        creds_data = json.load(f)

    creds = Credentials(
        token=creds_data.get("token"),
        refresh_token=creds_data.get("refresh_token"),
        token_uri=creds_data.get("token_uri"),
        client_id=creds_data.get("client_id"),
        client_secret=creds_data.get("client_secret"),
        scopes=creds_data.get("scopes") or SCOPES,
    )

    return build("calendar", "v3", credentials=creds)
