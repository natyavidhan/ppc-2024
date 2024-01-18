from faster_whisper import WhisperModel
model = WhisperModel("medium", device="cuda", compute_type="float16")
print(model.transcribe("/recording0.wav", beam_size=5)[0]['text'])
