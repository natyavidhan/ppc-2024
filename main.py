import cv2
from deepface import DeepFace

cap = cv2.VideoCapture(1)

h=[0, 0, 0]

print("starting")

while True:
    try:
        ret, frame = cap.read()

        predictions = DeepFace.analyze(frame, actions=['emotion'], detector_backend="retinaface")
        emotion = predictions[0]['dominant_emotion']
        
        x, y, w, h_ = predictions[0]['region'].values()
        face_roi = frame[y:y+h_, x:x+w]
        
        # cv2.imshow('Emotion Detection', face_roi)
        print(".", end=" ")
        h.pop(0)
        h.append(emotion)

    except Exception as e:
        # print("error", e)
        print("_", end=" ")
        h.pop(0)
        h.append(0)

    if h[0] == h[1] == h[2] != 0:
        print(f"\nHello there! you look {h[0]}\n")
        h = [0, 0, 0]

    if cv2.waitKey(1) == ord('q'):
        break
    # print("yes")

cap.release()
cv2.destroyAllWindows()
