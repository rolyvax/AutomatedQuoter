# weather.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# (tercihen) otomatik driver yönetimi: pip install webdriver-manager
from selenium.webdriver.chrome.service import Service
try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WDM = True
except Exception:
    USE_WDM = False


class Weather:
    def __init__(self, il="İstanbul", ilce="Pendik", headless=True):
        self.url = f"https://www.mgm.gov.tr/tahmin/il-ve-ilceler.aspx?il={il}&ilce={ilce}"
        self.headless = headless
        self.records = []
        self._scrape()

    # --- emoji yardımcıları ---
    def _normalize(self, s: str) -> str:
        return s.strip().lower()

    def _emoji_from_phrase(self, phrase: str) -> str:
        if not phrase:
            return "🔆"
        p = self._normalize(phrase)

        exact = {
            "güneşli": "☀️",
            "çoğunlukla güneşli": "🌤️",
            "parçalı güneşli": "⛅",
            "aralıklı bulutlar": "🌥️",
            "çoğunlukla bulutlu": "☁️",
            "çok bulutlu": "☁️",
            "bulutlu": "☁️",
            "kasvetli": "🌫️",
            "sisli": "🌁",
            "yağmurlu": "🌧️",
            "sağanak yağışlı": "🌦️",
            "gök gürültülü sağanak yağışlı": "⛈️",
            "karlı": "❄️",
            "sulu kar": "🌨️",
            "buzlu": "🧊",
            "rüzgarlı": "💨",
            "sıcak": "🔥",
            "soğuk": "🥶",
        }
        if p in exact:
            return exact[p]

        contains = [
            ("gök gürültülü", "⛈️"),
            ("sağanak", "🌦️"),
            ("yağış", "🌧️"),
            ("karlı", "❄️"),
            ("sulu kar", "🌨️"),
            ("sis", "🌁"),
            ("çok bulutlu", "☁️"),
            ("çoğunlukla bulutlu", "☁️"),
            ("bulut", "☁️"),
            ("parçalı güneş", "⛅"),
            ("güneş", "☀️"),
            ("rüzgar", "💨"),
            ("sıcak", "🔥"),
            ("soğuk", "🥶"),
        ]
        for key, emo in contains:
            if key in p:
                return emo
        return "🔆"

    # --- ana scrape ---
    def _scrape(self):
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("--headless=new")  # Chrome 109+
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--disable-notifications")

        if USE_WDM:
            service = Service(ChromeDriverManager().install())
        else:
            # Sistemde yüklü chromedriver varsa bu şekilde bırak.
            service = Service()

        driver = webdriver.Chrome(service=service, options=options)
        driver.get(self.url)

        wait = WebDriverWait(driver, 25)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr")))

        rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")[1:]  # başlığı atla

        def parse_hour(hhmm: str) -> int:
            return int(hhmm.split(".")[0])

        # hedef gün: ilk veri satırındaki gün adı
        if rows:
            first_spans = rows[0].find_elements(By.CSS_SELECTOR, "th span.ng-binding")
            target_day = first_spans[0].text.strip() if len(first_spans) >= 1 else None
        else:
            target_day = None

        out = []
        for row in rows:
            spans = row.find_elements(By.CSS_SELECTOR, "th span.ng-binding")
            if len(spans) < 3:
                continue

            gun_adi = spans[0].text.strip()
            onceki_saat = spans[1].text.strip()
            sonraki_saat = spans[2].text.strip()

            # sadece ilk gün
            if target_day and gun_adi != target_day:
                break

            # 09–24 aralığı
            start_h = parse_hour(onceki_saat)
            if start_h < 9 or start_h > 23:
                continue

            # hadise
            try:
                hadise_title = row.find_element(
                    By.CSS_SELECTOR, "td:nth-of-type(1) img[title]"
                ).get_attribute("title").strip()
            except:
                hadise_title = None

            # sıcaklıklar (xT: [sicaklik, hissedilen])
            xT_spans = row.find_elements(By.CSS_SELECTOR, "td.xT span")
            sicaklik = xT_spans[0].text.strip() if len(xT_spans) > 0 else None
            hissedilen = xT_spans[1].text.strip() if len(xT_spans) > 1 else None

            out.append({
                "gun": gun_adi,
                "onceki_saat": onceki_saat,
                "sonraki_saat": sonraki_saat,
                "sicaklik": sicaklik,
                "hissedilen": hissedilen,
                "hadise": hadise_title,
                "emoji": self._emoji_from_phrase(hadise_title),
            })

        try:
            driver.quit()
        except:
            pass

        self.records = out

    def get_forecast(self):
        return self.records
