from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, os, requests

class News:
    def __init__(self):
        load_dotenv()

        def make_haber(haber):
            haber_lines = haber.text.split('\n')
            haber_source = haber_lines[0]
            try:
                haber_text = haber_lines[2]
            except IndexError:
                haber_text = haber_lines[1] if len(haber_lines) > 1 else "Başlık bulunamadı"
            haber_link = haber.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

            return (f"<br>{'-' * 80}<br><b>Başlık:</b> {haber_text}<br>"
                    f"<b>Kaynak:</b> {haber_source}<br>"
                    f"<b>URL:</b> <a href='{haber_link}'>Haberi okumak için tıklayınız.</a>")

        BUNDLE_URL = 'https://www.bundle.app/'

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.haberler = []

        driver = webdriver.Chrome(options=chrome_options)
        try:
            # Gündem
            driver.get(BUNDLE_URL + "gundem")
            time.sleep(2)
            tum_haberler = driver.find_elements(by=By.CSS_SELECTOR, value='.owl-stage > .owl-item.active > .newsSliderCard')
            self.haberler.append(f"<br><br><b>Gündem Haberleri:</b>")
            for haber in tum_haberler:
                self.haberler.append(make_haber(haber))

            # Finans
            driver.get(BUNDLE_URL + "finans")
            time.sleep(2)
            tum_haberler = driver.find_elements(by=By.CSS_SELECTOR, value='.owl-stage > .owl-item.active > .newsSliderCard')
            self.haberler.append(f"<br>{'-' * 80}<br><br><b>Finans Haberleri:</b>")
            for haber in tum_haberler:
                self.haberler.append(make_haber(haber))

            # Spor
            driver.get(BUNDLE_URL + "spor")
            time.sleep(2)
            tum_haberler = driver.find_elements(by=By.CSS_SELECTOR, value='.owl-stage > .owl-item.active > .newsSliderCard')
            self.haberler.append(f"<br>{'-' * 80}<br><br><b>Spor Haberleri:</b>")
            for haber in tum_haberler:
                self.haberler.append(make_haber(haber))

        finally:
            driver.quit()

    def get_exchange_rates(self):
        load_dotenv()
        API_KEY = os.getenv("EXCHANGE_API")

        if not API_KEY:
            raise Exception("🚨 EXCHANGERATE_APIKEY not found in .env")

        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
        response = requests.get(url)
        data = response.json()

        if data.get("result") != "success":
            raise Exception(f"ExchangeRate-API Error: {data.get('error-type', 'Unknown')}")

        usd_try = data["conversion_rates"]["TRY"]
        usd_eur = data["conversion_rates"]["EUR"]
        eur_try = usd_try / usd_eur

        usd_try = round(usd_try, 2)
        eur_try = round(eur_try, 2)

        return usd_try, eur_try
