import cv2
from deepface import DeepFace
import pyttsx3
from bardapi import BardCookies
import speech_recognition as sr
from dotenv import load_dotenv
from datetime import datetime
import pygame
import numpy as np
import browser_cookie3

# --disable-features=LockProfileCookieDatabase

def get_cookies(domain):
    Cookies={}
    chromeCookies = list(browser_cookie3.chrome())
    for cookie in chromeCookies:
        if (domain in cookie.domain):
            Cookies[cookie.name]=cookie.value
    return Cookies

log = lambda x: print(f"[{datetime.now()}] {x}")

log("Anisha Booting up")
log("loading environment variables")
load_dotenv()

log("Setting up video capture device")
cap = cv2.VideoCapture(0)

log("Setting up Bard")
bard = BardCookies(cookie_dict=get_cookies(".google.com"))

log("Setting up text-to-speech engine")
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 1.0)
engine.setProperty('rate', 170) 

log("Setting up voice recognizer")
r = sr.Recognizer()

log("setting up window")
pygame.font.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
running = True

font = pygame.font.Font("Comfortaa.ttf", 38)

h = pygame.display.Info().current_h
w = pygame.display.Info().current_w

his=[0, 0, 0]
state = "see"
emotion = None
conversation = []
backend = "mediapipe"
current_text=""
current_speaker=""

def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1
        # if y + fontHeight > rect.bottom:
        #     break
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1     
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
        surface.blit(image, (rect.left-(rect.width//2), y-(rect.height//2)))
        y += fontHeight + lineSpacing
        text = text[i:]

    return text

def screen_cycle():
    screen.fill((255, 255, 255))

    head = pygame.font.Font("Comfortaa.ttf", 96).render("Anisha", True, (0, 0, 0))
    rect = head.get_rect()
    rect.center = (w // 2, h // 12)
    screen.blit(head, rect)

    c = font.render(f"Speaker: {current_speaker}", True, (0, 0, 0))
    rect = c.get_rect()
    rect.center = (w // 2, h //1.8)
    screen.blit(c, rect)

    try:
        _, frame = cap.read()
        frame = np.rot90(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame)
    except:
        frame = pygame.Surface((320, 240))
    rect = frame.get_rect() 
    rect.center = (w // 2, h // 3)
    rect.width = 320
    rect.height = 240
    screen.blit(frame, rect)

    text_rect = pygame.Rect(w // 2, h // 1.2, 800 / 1080 * w, 960 / 1920 * h)
    drawText(screen, current_text, (0, 0, 0), text_rect, pygame.font.Font("Comfortaa.ttf", 24))
    pygame.display.update()

def change_text(speaker, text):
    global current_text
    global current_speaker
    current_speaker=speaker
    current_text = text
    screen_cycle()

def speak(text):
    change_text("Anisha", text)
    engine.say(text)
    engine.runAndWait()

def ask_user():
    log("Asking user")
    moveon = False
    while not moveon:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            try:
                change_text("User", "Recognizing Voice...")
                screen_cycle()
                with sr.Microphone() as source:
                    audio = r.listen(source, phrase_time_limit=5)
                query = r.recognize_google(audio)
                screen_cycle()
                change_text("User", query)
                screen_cycle()
                moveon = True
                return query
            except sr.exceptions.UnknownValueError:
                log("[ERROR] Couldn't hear user, Attempting again...")
                speak("Sorry, can you please repeat yourself?")
                return ask_user()
        else:
            screen_cycle()

def ask_bard(query):
    ans = bard.get_answer(query)['content'].replace("*", "")
    return ans

def conversate(text, side):
    global conversation
    conversation.append(("bot" if side == 0 else "user", text))

def see():
    print("seeing user")
    try:
        print("test")
        ret, frame = cap.read()
        predictions = DeepFace.analyze(frame, actions=['emotion'], detector_backend=backend)
        emotion = predictions[0]['dominant_emotion']

        # x, y, w, h_ = predictions[0]['region'].values()
        # face_roi = frame[y:y+h_, x:x+w]

        his.pop(0)
        his.append(emotion)

    except ValueError as e:
        print(e)
        his.pop(0)
        his.append(0)

def approach():
    global state
    speak(f"Hello There! Your current emotion is {emotion}, Do you want me to help you with anything?")
    user = ask_user()
    agree = ask_bard(f"Tell me if the following is agreeing or not, ONLY OUTPUT TRUE OR FALSE, AND NOTHING ELSE \n{user}")
    
    if "false" in agree.lower():
        speak("Oh okay, have a nice day!")
        change_text("", "")
        state="see"
    else:
        state = "interact"

def interact():
    global state
    global conversation
    if len(conversation) == 0:
        text = "Okay, Let me introduce myself first, my name is anisha, I am your personal AI stress relieving assistant, please tell me about your problem so i can help you with that."
    else:
        text = "Do you have anymore questions? please answer in positive or negative tone"
        speak(text)
        user = ask_user()
        agree = ask_bard(f"Tell me if the following is agreeing or not, ONLY OUTPUT TRUE OR FALSE, AND NOTHING ELSE \n{user}")
        if "false" in agree.lower():
            speak("Oh okay, have a nice day!")
            change_text("", "")
            state="see"
            conversation=[]
            return
        text = "Alright! Please tell me your query"

    speak(text)

    query = ask_user()

    conversate(query, 1)
    answer = ask_bard(f"""Create a comforting, supportive and short minimal solution as an AI stress reliever addressing the following user query: 

"{query}"
KEEP IT UNDER 100 WORDS, KEEP IT UNDER 100 WORDS, KEEP IT UNDER 100 WORDS, KEEP IT UNDER 100 WORDS
PROVIDE PLAIN TEXT RESPONSE ONLY, NO MARKDOWN, NO ASTERISKS NO EMOJIS NO IMAGES, DO NOT ASK THEM ANY QUESTIONS, JUST RESPOND WITH THE SOLUTION""")
    
    screen_cycle() 
    speak(answer) 
    conversate(answer, 0)


if __name__ == "__main__":
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen_cycle()
        if state == "see":
            see()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                if his[0] == his[1] == his[2] != 0:
                    state = "approach"
                    emotion = his[0]
                    his = [0, 0, 0]

        elif state == "approach":
            approach()

        elif state == "interact":
            interact()

        screen_cycle()