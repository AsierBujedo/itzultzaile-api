import pycurl
import json
from bs4 import BeautifulSoup

TEXT_URL = "https://itzuli.api.euskadi.eus/ac65aDictionaryWar/DictionaryWS/getSpanishTranslation"
AUDIO_URL = "https://api.euskadi.eus/itzuli/commander/do"
PHRASE_URL = "https://api.euskadi.eus/itzuli/es2eu/v2/translate"

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
    def build_word_request(self, word, origin_lang, dest_lang):
        return {
            "word": word,
            "originlang": origin_lang,
            "destinylang": dest_lang
        }

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

    def build_phrase_request(self, text):
        return {
            "mkey": "8d9016025eb0a44215c7f69c2e10861d",
            "text": text,
            "returnSentences": True
        }

    def translate_word(self, word):
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, TEXT_URL)
        curl.setopt(pycurl.HTTPHEADER, [f"{key}: {value}" for key, value in HEADERS.items()])
        curl.setopt(pycurl.POST, 1)
        curl.setopt(pycurl.POSTFIELDS, json.dumps(self.build_word_request(word, "es", "eu")))
        response_buffer = bytearray()
        curl.setopt(pycurl.WRITEFUNCTION, response_buffer.extend)
        curl.perform()
        curl.close()
        return response_buffer.decode('utf-8')

    def get_first_translation_word(self, html):
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

    def translate_phrase(self, text):
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, PHRASE_URL)
        curl.setopt(pycurl.HTTPHEADER, [f"{key}: {value}" for key, value in HEADERS.items()])
        curl.setopt(pycurl.POST, 1)
        curl.setopt(pycurl.POSTFIELDS, json.dumps(self.build_phrase_request(text)))
        response_buffer = bytearray()
        curl.setopt(pycurl.WRITEFUNCTION, response_buffer.extend)
        curl.perform()
        curl.close()
        return response_buffer.decode("utf-8")

    def extract_phrase_translation(self, response_json_str):
        try:
            data = json.loads(response_json_str)
            return data.get("translation", "")
        except json.JSONDecodeError:
            return ""

    def text_to_speech(self, text):
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, AUDIO_URL)
        curl.setopt(pycurl.HTTPHEADER, [f"{key}: {value}" for key, value in HEADERS.items()])
        curl.setopt(pycurl.POST, 1)
        curl.setopt(pycurl.POSTFIELDS, json.dumps(self.build_audio_request(text)))
        response_buffer = bytearray()
        curl.setopt(pycurl.WRITEFUNCTION, response_buffer.extend)
        curl.perform()
        curl.close()
        return response_buffer

def save_audio(audio_bytes, filename="audio.wav"):
    with open(filename, "wb") as f:
        f.write(audio_bytes)
