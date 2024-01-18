import cv2
from deepface import DeepFace

face_cascade = cv2.CascadeClassifier('C:/Users/Blessbini/AppData/Local/Programs/Python/Python39/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(1)

while True:
    try:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_roi = frame[y:y+h, x:x+w]
            try:
                predictions = DeepFace.analyze(face_roi, actions=['emotion'])
                emotion = predictions[0]['dominant_emotion']
                # print(predictions)
                cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            except Exception as e:
                # print(f"Error: {e}")
                pass
        cv2.imshow('Emotion Detection', frame)
    except:
        pass

        

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
