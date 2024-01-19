import pyttsx3
engine = pyttsx3.init()
from bardapi import BardCookies
import speech_recognition as sr

print("start")
print()


cookie_dict = {
    "__Secure-1PSID": "egjP4T18AjffIk2CBL3i_Rf_XWHdyyRfM9uonNn-ih7HsSGeUKhIAKNEyrHqdEulqxdJNQ.",
    "__Secure-1PSIDTS": "sidts-CjIBPVxjSgE0nPdG9ALtEvWPNTrPdTTsjGBjdli-lnkJgbjPt7e77Cnk037KFByBkA2HixAA",
    "__Secure-1PSIDCC": "ABTWhQGnXcnotJkWb9jfomtkeOfqJuf7QQLMMz3XlVPckv_uQit3g7rBQFajArAAqKQWhPRZMw",
    "__Secure-1PAPISID": "10DU3mWwvXrka-zg/A9xlK92-wiDEFzGzT",
    # Any cookie values you want to pass session object.
}

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

    print("processng...")

    ans = bard.get_answer(query)['content']

    engine.say(ans)
    engine.runAndWait()
