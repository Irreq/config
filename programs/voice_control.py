import os
import speech_recognition as sr

def notify(response):
    #print(response)
    os.system('sam "{}"'.format(response))

def parse_query(query):
    if query.startswith("hello"):
        notify("Hello, Isac")
    elif query.startswith("exit"):
        notify("Shutting down, please come back again!")
        exit(0)
    # elif query.startswith("terminal"):
    else:
        import nltk
        tokenized = nltk.word_tokenize(query)
        nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if (pos[:2] == 'NN')]
        notify(" ".join(nouns))
        notify("I'm terribly sorry, but I cannot help you with that.")

def recognize_speech_from_microphone(recognizer, microphone):
    response = {
            "success": True,
            "error": "",
            "transcription": ""
    }

    if not isinstance(recognizer, sr.Recognizer):
        response["error"] = "`recognizer` must be `Recognizer` instance"

    if not isinstance(microphone, sr.Microphone):
        response["error"] = "`microphone` must be `Microphone` instance"

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        data = recognize_speech_from_microphone(recognizer, microphone)
        if data["error"] != "":
            notify(data["error"])
        else:
            parse_query(data["transcription"])
