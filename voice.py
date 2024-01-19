import pyttsx3
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 1.0)
engine.setProperty('rate', 125) 
engine.say("Okay, Let me introduce myself first, my name is anaya, I am your personal AI stress relieving assistant, please tell me about your problem so i can help you with that.")
engine.runAndWait()

# voices = engine.getProperty('voices')
# for v in voices:
#     print(v)