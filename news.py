import time
import os
import re
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class News:
    def __init__(self):
        load_dotenv()
        self.haberler = []

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=chrome_options)

        try:
            self.driver.get("https://news.google.com/home?hl=tr&gl=TR&ceid=TR:tr")
            time.sleep(3)

            containers = self.driver.find_elements(By.CLASS_NAME, "KDoq1")[:5]  # 5 bloğu al, istersen değiştir

            for index, container in enumerate(containers, start=1):
                try:
                    article = container.find_element(By.TAG_NAME, "article")
                    link_candidates = article.find_elements(By.TAG_NAME, "a")

                    a_el = None
                    for a in link_candidates:
                        if a.get_attribute("aria-label") and a.get_attribute("href"):
                            a_el = a
                            break

                    if not a_el:
                        print(f"[{index}] Uygun haber bağlantısı bulunamadı.")
                        continue

                    href = a_el.get_attribute("href")
                    label = a_el.get_attribute("aria-label")

                    title_match = re.search(r"^(.*?) - ", label)
                    source_match = re.findall(r" - ([^-]+) - ", label)

                    title = title_match.group(1) if title_match else "Başlık bulunamadı"
                    source = source_match[0] if source_match else "Kaynak bulunamadı"

                    try:
                        time_el = article.find_element(By.TAG_NAME, "time")
                        iso_time = time_el.get_attribute("datetime")
                        dt = datetime.fromisoformat(iso_time.replace("Z", "+00:00"))
                        dt_local = dt + timedelta(hours=3)
                        date_str = dt_local.strftime("%d %B %Y %H:%M")
                    except:
                        date_str = "Tarih alınamadı"

                    link = "https://news.google.com" + href[1:] if href.startswith("./") else href

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

        finally:
            self.driver.quit()

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
