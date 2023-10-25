with sr.Microphone() as source:
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