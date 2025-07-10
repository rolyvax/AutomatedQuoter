import os, requests, time
from dotenv import load_dotenv

class Weather:
    def __init__(self):
        load_dotenv()

        API_KEY = os.getenv("ACCUWEATHER_APIKEY")

        # Step 1: Get location key for Istanbul
        location_url = "http://dataservice.accuweather.com/locations/v1/cities/search"
        loc_params = {
            "apikey": API_KEY,
            "q": "Istanbul"
        }

        response = requests.get(location_url, params=loc_params)
        location_data = response.json()
        istanbul_key = location_data[0]['Key']

        # Step 2: Get daily forecast
        forecast_url = f'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{istanbul_key}'
        fcast_params = {
            "apikey": API_KEY,
            "language": "tr-tr",
            "metric": True,
        }

        response = requests.get(url=forecast_url, params=fcast_params)
        forecast_data = response.json()

        self.min_temp = forecast_data['DailyForecasts'][0]['Temperature']['Minimum']['Value']
        self.max_temp = forecast_data['DailyForecasts'][0]['Temperature']['Maximum']['Value']
        self.day_sky = forecast_data['DailyForecasts'][0]['Day']['IconPhrase']
        self.night_sky = forecast_data['DailyForecasts'][0]['Night']['IconPhrase']
        self.day_emoji = self.get_day_emoji(self.day_sky)
        self.night_emoji = self.get_night_emoji(self.night_sky)

    def get_day_emoji(self, phrase):
        return {
            "Güneşli": "☀️",
            "Çoğunlukla güneşli": "🌤️",
            "Parçalı güneşli": "⛅",
            "Aralıklı bulutlar": "🌥️",
            "Çoğunlukla bulutlu": "☁️",
            "Bulutlu": "🌫️",
            "Kasvetli": "🌫️",
            "Sisli": "🌁",
            "Yağmurlu": "🌧️",
            "Sağanak yağışlı": "🌦️",
            "Gök gürültülü sağanak yağışlı": "⛈️",
            "Karlı": "❄️",
            "Sulu kar": "🌨️",
            "Buzlu": "🧊",
            "Rüzgarlı": "💨",
            "Sıcak": "🔥",
            "Soğuk": "🥶",
        }.get(phrase, "🔆")

    def get_night_emoji(self, phrase):
        return {
            "Açık": "🌙",
            "Çoğunlukla açık": "🌖",
            "Parçalı bulutlu": "🌤️",
            "Aralıklı bulutlar": "🌥️",
            "Puslu ay ışığı": "🌫️",
            "Çoğunlukla bulutlu": "☁️",
            "Sağanak yağışlı": "🌧️",
            "Gök gürültülü sağanak yağışlı": "⛈️",
            "Karlı": "❄️",
            "Sulu kar": "🌨️",
            "Rüzgarlı": "💨",
            "Sisli": "🌁",
        }.get(phrase, "🌌")  # default to night sky

# Test
if __name__ == "__main__":
    weather = Weather()
    print(f"Gündüz: {weather.day_sky} {weather.day_emoji}")
    print(f"Gece: {weather.night_sky} {weather.night_emoji}")
    print(f"Minimum: {weather.min_temp}°C")
    print(f"Maksimum: {weather.max_temp}°C")
