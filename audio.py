import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv


freq = 44100

# Recording duration
duration = 5

recording = sd.rec(int(duration * freq), 
                   samplerate=freq, channels=2)

# Record audio for the given number of seconds
sd.wait()

write("recording0.wav", freq, recording)