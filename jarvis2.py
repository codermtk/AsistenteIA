from openai import OpenAI
from dotenv import load_dotenv
import os
import speech_recognition as sr
import pyttsx3



# Carga las variables de entorno y la clave de la API
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

# Inicializa el reconocedor de voz
r = sr.Recognizer()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

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

# Función para enviar mensajes y obtener respuestas, manteniendo el historial
def chat_with_ai():
    messages = [
        {"role":"system","content":"Te llamas Atenea y eres un asistente personal."}
    ]
    initial_message = "¿En qué puedo ayudarte?"

    print(initial_message)
    speak(initial_message)

    while True:
        user_message = listen()
        if user_message.lower() == "stop":
            break

        if len(messages) > 6:  # Más de 3 parejas de mensajes
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
