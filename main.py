# main.py
import asyncio
from dotenv import load_dotenv

from songs import Songs
from quoter import Quoter
from mailer import Mailer
from news import News
from todaysimportant import TodaysImportant
from weather import Weather

load_dotenv()

song = Songs()
news = News()
quoter_instance = Quoter()
mailer = Mailer()
important = TodaysImportant()

# Yeni Weather'dan kayıtları çek
weather = Weather(il="İstanbul", ilce="Pendik", headless=True)
records = weather.get_forecast()  # [{'gun','onceki_saat','sonraki_saat','sicaklik','hissedilen','hadise','emoji'}, ...]

def _to_float(x):
    try:
        return float(str(x).replace(",", "."))
    except Exception:
        return None

# min/max (saatlik sıcaklıklardan)
temps = [_to_float(r.get("sicaklik")) for r in records if _to_float(r.get("sicaklik")) is not None]
min_temp = min(temps) if temps else None
max_temp = max(temps) if temps else None

# sabah/akşam özetleri (ilk ve son blok)
if records:
    sabah_durumu = records[0].get("hadise")
    sabah_emoji  = records[0].get("emoji", "")
    aksam_durumu = records[-1].get("hadise")
    aksam_emoji  = records[-1].get("emoji", "")
else:
    sabah_durumu = sabah_emoji = aksam_durumu = aksam_emoji = ""

# Eski değişken isimleriyle uyumlu yazdırma (None güvenliği)
_safe_max = f"{max_temp:5.1f}" if isinstance(max_temp, float) else "--"
_safe_min = f"{min_temp:5.1f}" if isinstance(min_temp, float) else "--"

# Saatlik blokların metni
lines = []
for r in records:
    line = (
        f"{r['onceki_saat']:>5} - {r['sonraki_saat']:<5}  |  "
        f"{(r['sicaklik'] or '--'):>2}° / {(r['hissedilen'] or '--'):>2}°  |  "
        f"{(r['hadise'] or '')} {r.get('emoji','')}"
    )
    lines.append(line)
blocks_text = "\n".join(lines) if lines else "Veri bulunamadı."

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
          line-height: 1.35;
       }}
       .muted {{
          color: #666;
       }}
    </style>
  </head>
  <body>
    <pre class="weather">
<u>09:00 – 24:00 arası hava durumu:</u>
{blocks_text}
    </pre>
  </body>
</html>
"""

usd, eur = news.get_exchange_rates()

async def main():
    translated_quote = quoter_instance.get_translated_quote()
    the_song = (song.song_name, song.song_link, song.song_artist)
    full_translated = f"{translated_quote} - {quoter_instance.author}"
    original_quote = quoter_instance.full_quote

    # mail gönderimi (senin eski imzanla aynı sırada)
    mailer.send_email(
        original_quote,
        full_translated,
        news.haberler,
        weather_report,
        important.events,
        the_song,
        usd,
        eur
    )

# çalıştır
asyncio.run(main())
