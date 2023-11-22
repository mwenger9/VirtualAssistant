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


class ScenarioManager:


      french_stopwords : set = {}
      keyword_scenario_mapping : dict = {}

      def __init__(self) -> None:

            with open("stopwords.json",encoding='utf8') as stopwords_fp, open("keyword_scenario_mapping.json",encoding="utf8") as scenarios_fp:
                  self.french_stopwords = set(json.load(stopwords_fp)["french"])
                  self.keyword_scenario_mapping = json.load(scenarios_fp)
            

      def parse_request(self,request : str) -> str:
            request = request.lower()
            request = re.sub(r'[^\w\s]', ' ', request)
            request = request.strip()
            request = re.split(r"[ -]", request)
            request = [word for word in request if not word in self.french_stopwords]

            for word in request :
                  if self.keyword_scenario_mapping.get(word,None):
                        return self.keyword_scenario_mapping.get(word)



if __name__ == "__main__":

      download("punkt")

      scenarioManager = ScenarioManager()


      res  = scenarioManager.parse_request("Quel temps fait-il à Tokyo ?")
      print(res)

      res  = scenarioManager.parse_request("Je souhaite connaitre la météo.")
      print(res)

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



