import speech_recognition as sr
from gtts import gTTS
import os
import json
import requests
from playsound import playsound


def speak(text):
    tts = gTTS(text=text, lang='fr')
    tts.save("temp.mp3")
    playsound("temp.mp3")
    os.remove("temp.mp3")

if __name__ == "__main__":
    with open("credentials.json") as json_file:
        API_key = json.load(json_file)["weather"]

    lat,lon = 48.11707303093078, -1.6815776506872837
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_key}'
    #url = f'https://api.openweathermap.org/data/2.5/weather?q=sRenne&units=metric&appid={API_key}'
    response = requests.get(url).json()
    speak(f"Il fait {response['main']['temp']}°C à {response['name']}")
