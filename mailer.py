import smtplib
import locale
from email.utils import formataddr
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()


class Mailer:
    def __init__(self):
        try:
            locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')  # Set locale to Turkish
        except locale.Error:
            print("Turkish locale not found, defaulting to system locale.")

        today = datetime.today()
        self.formatted_date = today.strftime('%d-%b-%Y')


    def send_email(self, translated_quote, quote, haberler, weather, events, song, usd, eur):
        sender_email = "astelaxrolyvax@gmail.com"
        receiver_emails = ["hakanakay@kabinet.com.tr"]
        password = os.getenv('GMAIL_PASS')

        # Email content (formatted with HTML tags)
        subject = f"{self.formatted_date} / Günlük Bilgi ve Durum Raporu."
        body = (f"<u>Güncel Döviz Kurları:</u><br>💵TRY/USD: {usd}<br>💶TRY/EUR: {eur}<br>"
                f"<br>{weather}"
                f"🎵Günün şarkısı: {song[2]} - {song[0]} - <a href={song[1]}>Spotify'da dinlemek için tıklayınız.🎵</a><br>"
                f"<br><i>{translated_quote}</i><br>"
                f"<i>{quote}</i>"
                f"<br><br>{''.join(events)}"
                f"{''.join(haberler)}<br>{'-' * 80}<br><br><br>")

        # Set up the MIME for HTML
        sender_name = "Günün Fısıltısı"
        message = MIMEMultipart()
        message["From"] = formataddr((sender_name, sender_email))
        message["To"] = ", ".join(receiver_emails)
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))  # Ensure content type is 'html'

        # Send the email
        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)  # Gmail SMTP server
            server.login(sender_email, password)  # Log in to your email account
            server.sendmail(sender_email, receiver_emails, message.as_string())  # Send the email to multiple recipients
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            server.quit()  # Logout from the email server
