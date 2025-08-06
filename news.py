import os
import re
import time
import requests
import feedparser
from dotenv import load_dotenv


class News:
    def __init__(self):
        load_dotenv()
        self.haberler = []

        self.categories = {
            "Gündem": "https://news.google.com/rss/headlines/section/geo/Turkiye?hl=tr&gl=TR&ceid=TR:tr",
            "Dünya": "https://news.google.com/rss/headlines/section/topic/WORLD.tr_tr?hl=tr&gl=TR&ceid=TR:tr",
            "Spor": "https://news.google.com/rss/headlines/section/topic/SPORTS.tr_tr?hl=tr&gl=TR&ceid=TR:tr",
            "Finans": "https://news.google.com/rss/headlines/section/topic/BUSINESS.tr_tr?hl=tr&gl=TR&ceid=TR:tr",
        }

        self.fetch_all_categories(limit_per_category=3)

    def fetch_all_categories(self, limit_per_category=3):
        for category, url in self.categories.items():
            self.haberler.append(f"<br>{'-' * 120}<br><u><h4>📰 {category} Haberleri</h4></u>")
            news = self.fetch_news_rss(url, limit_per_category)
            self.haberler.extend(news)

    def fetch_news_rss(self, rss_url, limit):
        feed = feedparser.parse(rss_url)
        news_list = []

        for index, entry in enumerate(feed.entries[:limit], start=1):
            try:
                raw_title = entry.title
                title = re.sub(r"\s*-\s*[^-]+$", "", raw_title).strip()

                link = entry.link
                published = entry.published if 'published' in entry else "Tarih alınamadı"
                source = entry.source.title if 'source' in entry else "Kaynak yok"

                try:
                    pub_time = time.strptime(published, "%a, %d %b %Y %H:%M:%S %Z")
                    date_str = time.strftime("%d %B %Y %H:%M", pub_time)
                except:
                    date_str = published

                haber_html = (
                    f"<b>Başlık:</b> {title}<br>"
                    f"<b>Kaynak:</b> {source}<br>"
                    f"<b>Tarih:</b> {date_str}<br>"
                    f"<b>URL:</b> <a href='{link}'>Haberi okumak için tıklayınız.</a><br>"
                )

                if index > 1:
                    haber_html = "<br>" + haber_html  # Sadece ilk haber hariç önüne <br> koy

                news_list.append(haber_html)

            except Exception as e:
                print(f"[{index}] Haber alınamadı: {e}")
                continue

        return news_list

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
