from playwright.sync_api import sync_playwright

def get_next_week(lesson):
    with sync_playwright() as p:
        URL = f"https://voco.ee/tunniplaan/?course={lesson}"
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, wait_until="networkidle")
        page.wait_for_selector(".fc-time-grid")

        page.click(".fc-next-button")
        page.wait_for_timeout(700)

        dates = page.eval_on_selector_all(
            ".fc-time-grid .fc-bg td.fc-day[data-date]",
            "els => els.map(e => e.getAttribute('data-date'))"
        )

        items = []
        for e in page.query_selector_all(".fc-time-grid-event"):
            t = e.query_selector(".fc-time")
            title = e.query_selector(".fc-title")
            if not t or not title:
                continue

            full = t.get_attribute("data-full") or t.inner_text().strip()
            start, end = (full.split(" - ", 1) + [""])[:2]

            idx = e.evaluate("n => n.closest('td')?.cellIndex ?? 0")
            date = dates[idx - 1] if 0 < idx <= len(dates) else ""

            if date and start and end:
                items.append({
                    "date": date,
                    "start": start.strip(),
                    "end": end.strip(),
                    "title": title.inner_text().strip()
                })

        monday = dates[0] if dates else "unknown"
        browser.close()
        return monday, items
