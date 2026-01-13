# VOCO Timetable -> Google Calendar

Intended use is for adding a crontab on Friday what triggers the main.py at 18:00. 18:00 friday should be the day when the lesson plan gets locked. 

This project:
1) Opens the VOCO timetable page based on the id (can be manually gotten when selecting a grade and then getting it from the URL)
2) Scrapes the next week lessons (by default, if not changed)
3) Uploads them into your **Google Calendar**
4) Also saves an `.ics` file in `out/` (optional backup / manual import)

---

## Files

- `scraper.py`  
  Scrapes lessons and returns them as Python data.

- `csv_to_ics.py`  
  Turns the scraped lessons into an `.ics` file and uploads them to Google Calendar.

- `main.py`  
  Runs the whole flow: scrape -> upload.

---

## Requirements

- Python 3.10+ (3.11+ recommended)
- Google account
- Google Calendar API enabled

---
