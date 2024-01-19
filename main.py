import cv2
from deepface import DeepFace
import pyttsx3
from bardapi import BardCookies
import speech_recognition as sr
import json
import re
from dotenv import load_dotenv
import os
from datetime import datetime

log = lambda x: print(f"[{datetime().now()}] {x}")

log("Anisha v0.2")
log("loading environment variables")
load_dotenv()

log("Setting up video capture device")
cap = cv2.VideoCapture(0)

log("Setting up Bard")
cookie_dict = {i["name"]: i['value'] for i in json.load(open("cookies.json"))}
bard = BardCookies(cookie_dict=cookie_dict)

log("Setting up text-to-speech engine")
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 1.0)
engine.setProperty('rate', 125) 

log("Setting up voice recognizer")
r = sr.Recognizer()

h=[0, 0, 0]
state = "see"
emotion = None
conversation = []

def clean(text):
    pattern = r"[^\w.,0-9]+"
    return re.sub(pattern, "", text)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def ask_user():
    log("Asking user")
    try:
        with sr.Microphone() as source:
            print("<say>")
            audio = r.listen(source, phrase_time_limit=5)
        query = r.recognize_google(audio)
        return query
    except sr.exceptions.UnknownValueError:
        log("[ERROR] Couldn't hear user, Attempting again...")
        speak("Sorry, can you please repeat yourself?")
        return ask_user()

def ask_bard(query):
    ans = bard.get_answer(query + ". give short answer.")['content']
    return clean(ans)

def conversate(text, side):
    conversation.append(("bot" if side == 0 else "user", text))

def see():
    try:
        ret, frame = cap.read()
        predictions = DeepFace.analyze(frame, actions=['emotion'], detector_backend="retinaface")
        emotion = predictions[0]['dominant_emotion']
        
        # x, y, w, h_ = predictions[0]['region'].values()
        # face_roi = frame[y:y+h_, x:x+w]

        h.pop(0)
        h.append(emotion)

    except ValueError:
        h.pop(0)
        h.append(0)

def approach():
    global state
    speak(f"Hello There! Your current emotion is {emotion}, Do you want me to help you with anything?")
    user = ask_user()
    agree = ask_bard(f"Tell me if the following is agreeing or not, ONLY OUTPUT TRUE OR FALSE, AND NOTHING ELSE \n{user}")
    
    if "false" in agree.lower():
        speak("Oh okay, have a nice day!")
        state="see"
    else:
        state = "interact"

def interact():
    global state
    if len(conversation) == 0:
        text = "Okay, Let me introduce myself first, my name is anisha, I am your personal AI stress relieving assistant, please tell me about your problem so i can help you with that."
    else:
        text = "Do you have anymore questions? please answer in positive or negative tone"
        user = ask_user()
        agree = ask_bard(f"Tell me if the following is agreeing or not, ONLY OUTPUT TRUE OR FALSE, AND NOTHING ELSE \n{user}")
        if "false" in agree.lower():
            speak("Oh okay, have a nice day!")
            state="see"
            conversation=[]
            return
        text = "Alright! Please tell me your query"

    speak(text)

    query = ask_user()

    conversate(query, 1)
    answer = ask_bard("Create a comforting, supportive and short response as an AI stress reliever addressing the following user query: \n"+query)
    
    speak(answer)
    conversate(answer, 0)


if __name__ == "__main__":
    while True:
        if state == "see":
            see()
            if h[0] == h[1] == h[2] != 0:
                state = "approach"
                emotion = h[0]
                h = [0, 0, 0]

        elif state == "approach":
            approach()

        elif state == "interact":
            interact()