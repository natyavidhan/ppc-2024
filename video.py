import cv2
from deepface import DeepFace

cap = cv2.VideoCapture(1)


while True:
    try:
        ret, frame = cap.read()
        predictions = DeepFace.analyze(frame, actions=['emotion'], detector_backend="retinaface")
        emotion = predictions[0]['dominant_emotion']
        print(emotion)
        x, y, w, h = predictions[0]['region'].values()
        face_roi = frame[y:y+h, x:x+h]
        cv2.imshow('Emotion Detection', face_roi)
    except Exception as e:
        print("error", e)

        

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
