import pycurl
import json
from bs4 import BeautifulSoup

URL_TEXT = "https://itzuli.api.euskadi.eus/ac65aDictionaryWar/DictionaryWS/getSpanishTranslation"
URL_AUDIO = "https://api.euskadi.eus/itzuli/commander/do"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "application/json; charset=utf-8",
    "Origin": "https://www.euskadi.eus",
    "Connection": "keep-alive",
    "Referer": "https://www.euskadi.eus/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site"
}

class ServiceController:
    def build_request(self, word, origin_lang, dest_lang):
        return {
            "word": word,
            "originlang": origin_lang,
            "destinylang": dest_lang
        }

    def translate(self, text):
        c = pycurl.Curl()
        c.setopt(pycurl.URL, URL_TEXT)
        c.setopt(pycurl.HTTPHEADER, [f"{key}: {value}" for key, value in HEADERS.items()])
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.POSTFIELDS, json.dumps(self.build_request(text, "es", "eu")))
        response_buffer = bytearray()
        c.setopt(pycurl.WRITEFUNCTION, response_buffer.extend)
        c.perform()
        c.close()
        return response_buffer.decode('utf-8')

    def build_audio_request(self, text):
        return {
            "pipeline": "vicomtts_eu",
            "priority": 1,
            "input": f" \"{text}\" ",
            "config": {
                "vicomtts": {
                    "style": "nerea"
                }
            }
        }

    def to_audio(self, text):
        c = pycurl.Curl()
        c.setopt(pycurl.URL, URL_AUDIO)
        c.setopt(pycurl.HTTPHEADER, [f"{key}: {value}" for key, value in HEADERS.items()])
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.POSTFIELDS, json.dumps(self.build_audio_request(text)))
        response_buffer = bytearray()
        c.setopt(pycurl.WRITEFUNCTION, response_buffer.extend)
        c.perform()
        c.close()
        return response_buffer

def save_audio(audio_bytes, name="audio.wav"):
    with open(name, "wb") as f:
        f.write(audio_bytes)

def get_first_translation_word(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("div", class_="row")

    for div in rows:
        text = div.get_text(strip=True, separator=" ")
        if text and text[0].isdigit():
            parts = text.split(" ")
            for part in parts[2:]:
                word = part.strip(" ,;")
                if word:
                    return word
    return None

