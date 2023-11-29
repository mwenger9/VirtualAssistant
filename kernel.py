
from utils import *
from scenario_manager import ScenarioManager


if __name__ == "__main__":

    scen_manager = ScenarioManager()

    speak_playsound("Bonjour, en quoi puis-je vous aider")

    while True:
        try:
            req = listen_once()
            scen_manager.handle_and_execute_request(request=req)
            break
        except Exception as e:
            break