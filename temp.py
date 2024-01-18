import os, sys, time, json, cv2, datetime, subprocess
from deepface import DeepFace
import tensorflow.compat.v1.keras as keras
from tensorflow.compat.v1.keras.preprocessing import image
import numpy as np
from PIL import Image


emotions_model = keras.models.load_model("facial_expression.keras")

log = lambda x: print(f"[{datetime.datetime.now()}] {x}")


def emotion_analyse(img):
    img = image.load_img(img, grayscale=True, target_size=(48, 48))

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    x /= 255

    custom = emotions_model.predict(x)[0]
    return [float(i) for i in custom]


def gen_frames(path, output_dir, force):
    cap = cv2.VideoCapture(path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for count in range(0, frame_count, 1000):
        cap.set(cv2.CAP_PROP_POS_FRAMES, count)
        success, image = cap.read()
        if success:
            image_path = os.path.join(output_dir, f"{count}.jpg")
            cv2.imwrite(image_path, image)
            if force:
                break
    cap.release()


def face_match(reference_image_path, output_dir):
    for filename in os.listdir(output_dir):
        image_path = os.path.join(output_dir, filename)
        try:
            result = DeepFace.verify(
                img1_path=image_path, img2_path=reference_image_path, model_name = 'ArcFace', detector_backend = 'retinaface'
            )
            if result["distance"] < 0.4:
                return (result, image_path)
        except ValueError as e:
            # log(f"FATAL: {e}")
            pass
    return None


if __name__ == "__main__":
    streamer = sys.argv[1]
    force = False
    if len(sys.argv) == 3:
        if sys.argv[2] == "force":
            force = True
    streams = [i for i in os.listdir("data/" + streamer) if not i.endswith(".png")]

    for sno, stream in enumerate(streams):
        log(f"Processing stream '{stream}' ({sno})")

        path = f"data/{streamer}/{stream}"
        video_sgmt = path + "/video_segments"
        emotions = path + "/emotions.json"

        emotion_analysis_data = (
            json.load(open(emotions, "r", encoding="utf-8"))
            if os.path.exists(emotions)
            else []
        )

        if not os.path.exists(f"{path}/frames"):
            os.mkdir(f"{path}/frames")


        for b in [str(i).zfill(3) for i in range(len(os.listdir(video_sgmt)))][len(emotion_analysis_data):]:
            b_start = time.time()
            log(f"Batch no. {int(b)+1}/{len(os.listdir(video_sgmt))}")
            
            log("Generating frames")
            gen_frames(f"{video_sgmt}/{b}.mp4", f"temp/{stream}", force)

            if not force:
                log("Face Verification")
                face_frame = face_match(f"data/{streamer}/ref.png", f"temp/{stream}")

                if face_frame:
                    log("Face found, emotion analysis")
                    img = Image.open(face_frame[1])
                    k = face_frame[0]["facial_areas"]["img1"]
                    img = img.crop((k["x"], k["y"], k["x"] + k["w"], k["y"] + k["h"]))
                    img.save(f"{path}/frames/{b}.png")
                    emotion_audit = emotion_analyse(f"{path}/frames/{b}.png")
                else:
                    log("Face not found")
                    emotion_audit = [0, 0, 0, 0, 0, 0, 0]
            else:
                try:
                    emotion_audit = emotion_analyse(f"temp/{stream}/0.jpg")
                except FileNotFoundError:
                    emotion_audit = [0, 0, 0, 0, 0, 0, 0]
                    pass
            emotion_analysis_data.append(emotion_audit)
            
            for filename in os.listdir(f"temp/{stream}"):
                os.remove(os.path.join(f"temp/{stream}", filename))

            log(f"Batch processed in {time.time() - b_start}")

            json.dump(
                emotion_analysis_data, open(emotions, "w", encoding="utf-8"), indent=4
            )