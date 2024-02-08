from openai import OpenAI
from dotenv import load_dotenv
import os
import speech_recognition as sr
from gtts import gTTS
import playsound



# Carga las variables de entorno y la clave de la API
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

# Inicializa el reconocedor de voz
r = sr.Recognizer()

def speak(text):
    # Cambia el idioma a español ('es')
    tts = gTTS(text=text, lang='es', slow=False)
    tts.save("response.mp3")
    playsound.playsound("response.mp3")
    os.remove("response.mp3")

def listen():
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = r.listen(source)
        said = ""
        try:
            # Cambia el idioma a español ('es-ES')
            said = r.recognize_google(audio, language='es-ES')
            print(f"Tú dijiste: {said}")
        except Exception as e:
            print("Excepción: " + str(e))
    return said


def chat_with_ai():
    messages = [
        {"role":"system","content":"Te llamas Jarvis y eres un asistente personal."}
    ]
    initial_message = "¿En qué puedo ayudarte?"

    print(initial_message)
    speak(initial_message)

    while True:
        user_message = listen()
        if user_message.lower() == "stop":
            break

        if len(messages) > 6:  
            messages = messages[2:]
        
        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=messages
        )

        # Obtiene la respuesta de la API
        ai_message = response.choices[0].message.content
        print(f"IA: {ai_message}")
        speak(ai_message)

        messages.append({"role": "assistant", "content": ai_message})

        if len(messages) > 8:
            messages = messages[2:]

# Inicia el programa
chat_with_ai()
