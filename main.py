import asyncio
from songs import Songs
from dotenv import load_dotenv
from quoter import Quoter
from mailer import Mailer
from news import News
from weather import Weather
from todaysimportant import TodaysImportant
load_dotenv()

song = Songs()
news = News()
quoter_instance = Quoter()
mailer = Mailer()
weather = Weather()
important = TodaysImportant()

max_temp = weather.max_temp
min_temp = weather.min_temp
sabah_durumu = weather.day_sky
sabah_emoji = weather.day_emoji
aksam_durumu = weather.night_sky
aksam_emoji = weather.night_emoji
usd, eur = news.get_exchange_rates()

async def main():
    translated_quote = quoter_instance.get_translated_quote()
    the_song = (song.song_name, song.song_link)
    full_translated = f"{translated_quote} - {quoter_instance.author}"
    original_quote = quoter_instance.full_quote

    weather_report = f"""
    <html>
      <head>
        <style>
           body {{
        font-family: 'Calibri', sans-serif;
      }}
      pre.weather {{
        font-family: 'Consolas', 'Courier New', monospace;
        white-space: pre-wrap;
      }}
        </style>
      </head>
      <body>
        <pre>
<u>Bugünün hava durumu:</u> 
Maximum derece: {max_temp:5.1f}°C     Sabah hava durumu: {sabah_durumu} {sabah_emoji}
Minimum derece: {min_temp:5.1f}°C     Akşam hava durumu: {aksam_durumu} {aksam_emoji}
        </pre>
      </body>
    </html>
    """
    mailer.send_email(original_quote, full_translated, news.haberler, weather_report, important.events, the_song, usd, eur)


# Run the main async function
asyncio.run(main())

