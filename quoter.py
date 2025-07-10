import requests
from deep_translator import MyMemoryTranslator
import asyncio

class Quoter:
    def __init__(self):
        url = "https://zenquotes.io/api/today"
        self.response = requests.get(url)
        self.quote, self.author = self.get_motivational_quote()
        self.full_quote = f"{self.quote} - {self.author}"

    def get_motivational_quote(self):
        if self.response.status_code == 200:
            quote = self.response.json()[0]["q"]
            author = self.response.json()[0]["a"]
            return quote, author #f'"{quote}" - <b>{author}</b>'
        else:
            return "Could not fetch a quote."

    def translate_text(self, text):
        translated = MyMemoryTranslator(source='en-US', target='tr-TR').translate(text)
        return translated


    def get_translated_quote(self):
        return self.translate_text(self.quote)
