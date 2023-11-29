from nltk import download
import re
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
                  
      def handle_and_execute_request(self,request : str):
            parsed_scenario = self.parse_request(request)

            if parsed_scenario in globals() and isinstance(globals()[parsed_scenario], type):
                  scenario_instance = globals()[parsed_scenario]()
                  print(f"executing scenario {parsed_scenario}")
                  scenario_instance.execute()
            else:
                  print("Class not found.")




