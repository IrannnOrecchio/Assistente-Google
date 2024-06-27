import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup

# Função para reconhecer a fala usando o microfone
def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Diga algo:")
        audio = recognizer.listen(source)

    try:
        response = recognizer.recognize_google(audio, language='pt-BR')
        return response.strip()
    except sr.RequestError:
        return "API de reconhecimento de fala indisponível."
    except sr.UnknownValueError:
        return "Desculpe, não entendi o que você disse."

# Função para converter texto em fala
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Função para realizar uma pesquisa no Google baseada na pergunta
def search_google(question):
    try:
        search_query = question.lower()
        search_url = f"https://www.google.com/search?q={search_query}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        snippet = soup.find('div', class_='BNeawe')
        if snippet:
            return snippet.text
        else:
            return "Desculpe, não consegui encontrar uma resposta."
    except Exception as e:
        print("Erro ao pesquisar no Google:", e)
        return "Desculpe, ocorreu um erro ao buscar a resposta."

# Função principal para integrar todos os componentes
def main():
    while True:
        text = recognize_speech_from_mic()

        if text.lower() == "sair":
            speak_text("Até logo!")
            break

        print("Texto Reconhecido:", text)

        response_text = search_google(text)
        speak_text(response_text)

if __name__ == "__main__":
    main()
