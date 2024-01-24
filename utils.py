from gtts import gTTS
import os
from playsound import playsound
import speech_recognition as sr
import contextlib
import sys
from time import sleep
from TTS.api import TTS

#better_tts = TTS(model_name="tts_models/fr/css10/vits")

def speak(text):
    tts = gTTS(text=text, lang='fr')
    tts.save("temp.mp3")
    playsound("temp.mp3")
    sleep(0.2)
    os.remove("temp.mp3")

# def speak_better(text):
#     better_tts.tts_to_file(text)
#     playsound("output.wav")
#     os.remove("output.wav")


def speak_mmpg(text):
    tts = gTTS(text=text, lang='fr')
    tts.save("temp.mp3")
    os.system("mpg321 temp.mp3")
    os.remove("temp.mp3")

def speak_playsound(text):
    tts = gTTS(text=text, lang='fr')
    tts.save("temp.mp3")
    playsound("temp.mp3")
    os.remove("temp.mp3")

@contextlib.contextmanager
def ignoreStderr():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)



def listen():
    request = "start"
    with ignoreStderr():
        while request != "stop":
            # audio reco
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("En attente d'une instruction...")
                audio = r.listen(source)

            try:
                request = r.recognize_google(audio, language='fr-FR')
                print(request)
                return request
            except sr.UnknownValueError:
                print("Je n'ai pas bien compris")
                speak("Je n'ai pas bien compris")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                request = "stop"


def listen_once() -> str:
    request = "start"
    with ignoreStderr():
            # audio reco
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("En attente d'une instruction...")
            audio = r.listen(source)

        try:
            request = r.recognize_google(audio, language='fr-FR')
            print(request)
            return request
        except sr.UnknownValueError:
            print("Je n'ai pas bien compris")
            speak("Je n'ai pas bien compris")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))