import speech_recognition as sr
import utils
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk import download
import re
from nltk.stem import PorterStemmer
import json
import re

def parse_request(req):
       req = req.lower()
       req = re.sub(r'[^\w\s]', ' ', req)
       req = req.strip()
       req = re.split(r"[ -]", req)
       req = [word for word in req if not word in french_stopwords]

       for word in req:
              for scen in scenarios:
                    if word in scenarios[scen]["keywords"]:
                            print(f"Appel au scénario {scen}")
                            break


if __name__ == "__main__":

    download('stopwords')
    download("punkt")

    ps = PorterStemmer()

    r = sr.Recognizer()
    with open("stopwords.json",encoding='utf8') as stopwords_fp, open("scenarios.json",encoding="utf8") as scenarios_fp:
          french_stopwords = set(json.load(stopwords_fp)["french"])
          scenarios = json.load(scenarios_fp)


    parse_request("Quel temps fait-il à Tokyo ?")

    # with sr.Microphone() as source:
    #         print("En attente d'une instruction...")
    #         audio = r.listen(source)

    # try:
    #         request = r.recognize_google(audio, language='fr-FR')
    #         print(request)
    #         parse_request(request)
    # except sr.UnknownValueError:
    #         print("Je n'ai pas bien compris")
    # except sr.RequestError as e:
    #         print("Could not request results from Google Speech Recognition service; {0}".format(e))
    #         request = "stop"

    


