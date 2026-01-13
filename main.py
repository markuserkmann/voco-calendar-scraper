from scraper import get_next_week
from csv_to_ics import upload

week_monday, items = get_next_week()
ics_path, n = upload(week_monday, items)

print("Week:", week_monday)
print("Events:", n)
print("ICS:", ics_path)