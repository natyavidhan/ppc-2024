import pyttsx3
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 1.0)
engine.setProperty('rate', 125) 
engine.say("Good Morning mister narendra modei, we welcome you to the AI section of Kendriya Vidyalaya Sanghatan")
engine.runAndWait()

# voices = engine.getProperty('voices')
# for v in voices:
#     print(v)