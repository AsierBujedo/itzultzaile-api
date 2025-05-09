from service import service_controller as sc

service = sc.ServiceController()

def main():
    palabra = "programación"
    
    html = service.translate(palabra)
    primera = sc.get_first_translation_word(html)
    
    if primera:
        print(f"Traducción de {palabra}: {primera}")
        audio = service.to_audio(primera)
        sc.save_audio(audio, f"{primera}.wav")

if __name__ == "__main__":
    main()
