from service import service_controller as sc

service = sc.ServiceController()

def main():
    # An example for translating a word
    word = "Programacion"
    word_html = service.translate_word(word)
    translated_word = service.get_first_translation_word(word_html)
    print(f"Word '{word}' in Basque: {translated_word}")

    if translated_word:
        audio_word = service.text_to_speech(translated_word)
        sc.save_audio(audio_word, f"{translated_word}_word.wav")

    # Another example with a phrase
    phrase = "¿Te gusta programar en C?"
    phrase_json = service.translate_phrase(phrase)
    translated_phrase = service.extract_phrase_translation(phrase_json)
    print(f"Phrase '{phrase}' in Basque: {translated_phrase}")

    if translated_phrase:
        audio_phrase = service.text_to_speech(translated_phrase)
        sc.save_audio(audio_phrase, f"{translated_phrase}_phrase.wav")

if __name__ == "__main__":
    main()
