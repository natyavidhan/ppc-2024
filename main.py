import pyttsx3
engine = pyttsx3.init()
from bardapi import BardCookies
import speech_recognition as sr
import json

cookie_dict = {i["name"]: i['value'] for i in json.load(open("cookies.json"))}

bard = BardCookies(cookie_dict=cookie_dict)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 1.0)

while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source, phrase_time_limit=5)
    
    print("transcribing...")
    query = r.recognize_google(audio)

    print(f"Your query: {query}")

    print("processng...")

    ans = bard.get_answer(query + ". give a short answer")['content']

    engine.say(ans)
    engine.runAndWait()
