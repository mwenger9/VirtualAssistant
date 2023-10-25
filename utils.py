from gtts import gTTS
import os
from playsound import playsound

def speak(text):
    tts = gTTS(text=text, lang='fr')
    tts.save("temp.mp3")
    os.system("mpg321 temp.mp3")
    os.remove("temp.mp3")

def speak_playsound(text):
    tts = gTTS(text=text, lang='fr')
    tts.save("temp.mp3")
    playsound("temp.mp3")
    os.remove("temp.mp3")