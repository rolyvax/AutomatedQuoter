import requests
from datetime import datetime

class TodaysImportant:
    def __init__(self):
        today = datetime.now()
        self.events = self.get_on_this_day_events(today.month, today.day)

    def score_event(self, event):
        importance = 0
        text = event["text"].lower()

        high_priority = ["world war", "revolution", "president", "independence", "nuclear", "treaty"]
        mid_priority = ["beatles", "moon landing", "internet", "beethoven", "shakespeare", "coronation", "constitution"]
        low_priority = ["sports", "fashion", "tv show", "game", "album", "film"]

        if any(word in text for word in high_priority):
            importance += 3
        if any(word in text for word in mid_priority):
            importance += 2
        if any(word in text for word in low_priority):
            importance += 1

        if event["year"] < 1900:
            importance += 1

        return importance

    def get_on_this_day_events(self, month, day, top_n=3):
        url = f"https://tr.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}"
        response = requests.get(url)

        if response.status_code != 200:
            return [f"Failed to retrieve data: {response.status_code}"]

        data = response.json()
        events = data.get("events", [])

        scored_events = sorted(events, key=self.score_event, reverse=True)
        top_events = scored_events[:top_n]

        formatted = []
        for event in top_events:
            year = event["year"]
            text = event["text"]
            pages = event.get("pages", [])
            link = pages[0]["content_urls"]["desktop"]["page"] if pages else "https://tr.wikipedia.org"
            formatted.append(f"📅 {year} – {text}<br>")

        return formatted




