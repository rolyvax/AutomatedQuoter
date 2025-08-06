import os
import time
import requests
import feedparser
from dotenv import load_dotenv


class News:
    def __init__(self, limit=5):
        load_dotenv()
        self.haberler = []
        self.fetch_news_rss(limit)

    def fetch_news_rss(self, limit=5):
        rss_url = "https://news.google.com/rss?hl=tr&gl=TR&ceid=TR:tr"
        feed = feedparser.parse(rss_url)

        for index, entry in enumerate(feed.entries[:limit], start=1):
            try:
                title = entry.title
                link = entry.link
                published = entry.published if 'published' in entry else "Tarih alınamadı"
                source = entry.source.title if 'source' in entry else "Kaynak yok"

                # Yayın tarihi formatlama (varsa)
                try:
                    pub_time = time.strptime(published, "%a, %d %b %Y %H:%M:%S %Z")
                    date_str = time.strftime("%d %B %Y %H:%M", pub_time)
                except:
                    date_str = published

                self.haberler.append(
                    f"<br>{'-'*80}<br>"
                    f"<b>Başlık:</b> {title}<br>"
                    f"<b>Kaynak:</b> {source}<br>"
                    f"<b>Tarih:</b> {date_str}<br>"
                    f"<b>URL:</b> <a href='{link}'>Haberi okumak için tıklayınız.</a>"
                )

            except Exception as e:
                print(f"[{index}] Haber alınamadı: {e}")
                continue

    def build_email_html(self):
        return "".join(self.haberler)

    def get_exchange_rates(self):
        API_KEY = os.getenv("EXCHANGE_API")
        if not API_KEY:
            raise Exception("EXCHANGE_API key not found in .env")

        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
        response = requests.get(url)
        data = response.json()

        if data.get("result") != "success":
            raise Exception(f"ExchangeRate-API Error: {data.get('error-type', 'Unknown')}")

        usd_try = data["conversion_rates"]["TRY"]
        usd_eur = data["conversion_rates"]["EUR"]
        eur_try = usd_try / usd_eur

        return round(usd_try, 2), round(eur_try, 2)
