import cv2
from deepface import DeepFace
import pyttsx3
from bardapi import BardCookies
import speech_recognition as sr
import json
import re
from dotenv import load_dotenv
import os

print("Init")

load_dotenv()

cap = cv2.VideoCapture(0)

h=[0, 0, 0]

cookie_dict = {i["name"]: i['value'] for i in json.load(open("cookies.json"))}
bard = BardCookies(cookie_dict=cookie_dict)

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 1.0)
engine.setProperty('rate', 125) 

r = sr.Recognizer()

print("starting work cycle")

state = "see"
emotion_g = None

conversation = []

def gen_conv_str():
    return "\n\n\n".join(conversation)

def clean(text):
    pattern = r"[^\w.,0-9]+"
    return re.sub(pattern, "", text)

def ai(text):
    conversation.append(f"Helper: {text}")
    engine.say(text)
    engine.runAndWait()


def ask():
    try:
        with sr.Microphone() as source:
            print("<say>")
            audio = r.listen(source, phrase_time_limit=5)
        query = r.recognize_google(audio)
        return query
    except sr.exceptions.UnknownValueError:
        engine.say("Sorry, can you please repeat yourself?")
        engine.runAndWait()
        return ask()


def user(text):
    conversation.append(f"User: {text}")

def ask_bard(query, minimal=True) -> str:
    # conv = "speak as helper\n\n"
    # conv += gen_conv_str()
    # conv += "\n\nHelper:"
    return bard.get_answer(query + ". give short answer.")['content']

while True:
    if state == "see":
        # try:
        ret, frame = cap.read()

        predictions = DeepFace.analyze(frame, actions=['emotion'], detector_backend="retinaface")
        emotion = predictions[0]['dominant_emotion']
        
        x, y, w, h_ = predictions[0]['region'].values()
        face_roi = frame[y:y+h_, x:x+w]
        
        # cv2.imshow('Emotion Detection', face_roi)
        print(".")
        h.pop(0)
        h.append(emotion)

        # except Exception as e:
        #     print("error", e)
        #     print("_")
        #     h.pop(0)
        #     h.append(0)

        if h[0] == h[1] == h[2] != 0:
            state = "ask"
            emotion_g = emotion
            # print(f"\nHello there! you look {h[0]}\n")
            h = [0, 0, 0]

        # if cv2.waitKey(1) == ord('q'):
        #     break

    elif state == "ask":
        ai(f"Hello there, you look {emotion_g}. Do you want me to help you with anything?")
        query = ask()
        user(query)
        agree = ask_bard(f"Tell me if the following is agreeing or not, ONLY OUTPUT TRUE OR FALSE, AND NOTHING ELSE \n{query}")
        if "false" in agree.lower():
            engine.say("Oh okay, have a nice day!")
            engine.runAndWait()
            state="see"
        else:
            state = "interact"
        
    elif state == "interact":
        if len(conversation) == 2:
            text = "Okay, Let me introduce myself first, my name is anisha, I am your personal AI stress relieving assistant, please tell me about your problem so i can help you with that."
            # engine.say(text)
            ai(text)
        query = ask()
        user(query)
        ans = ask_bard(query)
        print(ans)
        ai(ans)


cap.release()
cv2.destroyAllWindows()
