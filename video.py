import cv2 , time
  
from keras.preprocessing import image
# import tensorflow.compat.v1.keras as keras
import numpy as np
import keras
model = keras.models.load_model("facial_expression.keras")
# define a video capture object 
vid = cv2.VideoCapture(1) 
  
while(True): 
      
    ret, im = vid.read() 
    cv2.imshow('frame', im) 
    cv2.imwrite("temp.jpg", im)

    img = image.load_img(
        "temp.jpg", grayscale=True, target_size=(48, 48)
    )
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = (x/255)

    custom = model.predict(x)[0]
    exp = {
        "angry": custom[0], 
        "disgust": custom[1], 
        "fear": custom[2], 
        "happy": custom[3], 
        "sad": custom[4], 
        "surprise": custom[5], 
        "neutral": custom[6]
    }

    sorted_dict = sorted(exp.items(), key=lambda item: item[1])
    print(sorted_dict)

    time.sleep(2)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 