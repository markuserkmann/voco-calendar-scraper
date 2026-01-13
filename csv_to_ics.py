import os
from datetime import datetime
from zoneinfo import ZoneInfo
from icalendar import Calendar, Event

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

TZ = ZoneInfo("Europe/Tallinn")
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

def dt(date_s, time_s):
    h, m = time_s.strip().replace(".", ":").split(":")
    return datetime.fromisoformat(f"{date_s}T{int(h):02d}:{int(m):02d}:00").replace(tzinfo=TZ)

def upload(week_monday, items, calendar_id="primary", secret_file="secret.json"):
    cal = Calendar()
    cal.add("prodid", "-//VOCO Plan//")
    cal.add("version", "2.0")

    for r in items:
        ev = Event()
        ev.add("summary", r["title"])
        ev.add("dtstart", dt(r["date"], r["start"]))
        ev.add("dtend", dt(r["date"], r["end"]))
        cal.add_component(ev)

    os.makedirs("out", exist_ok=True)
    ics_path = f"out/voco_{week_monday}.ics"
    with open(ics_path, "wb") as f:
        f.write(cal.to_ical())

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = InstalledAppFlow.from_client_secrets_file(secret_file, SCOPES).run_local_server(port=0)
        with open("token.json", "w", encoding="utf-8") as f:
            f.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)

    for r in items:
        start = dt(r["date"], r["start"])
        end = dt(r["date"], r["end"])
        service.events().insert(
            calendarId=calendar_id,
            body={
                "summary": r["title"],
                "start": {"dateTime": start.isoformat()},
                "end": {"dateTime": end.isoformat()},
            },
        ).execute()

    return ics_path, len(items)
