import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()

# import keras
import tensorflow.compat.v1.keras as keras
from tensorflow.compat.v1.keras.models import Sequential
from tensorflow.compat.v1.keras.layers import Conv2D, MaxPooling2D, AveragePooling2D
from tensorflow.compat.v1.keras.layers import Dense, Activation, Dropout, Flatten

from tensorflow.compat.v1.keras.preprocessing import image
from tensorflow.compat.v1.keras.preprocessing.image import ImageDataGenerator

import numpy as np
# import matplotlib.pyplot as plt

import keras as keras2

# ------------------------------
# cpu - gpu configuration
config = tf.ConfigProto(device_count={"GPU": 1, "CPU": 56})  # max: 1 gpu, 56 cpu
sess = tf.Session(config=config)
keras.backend.set_session(sess)

num_classes = 7  # angry, disgust, fear, happy, sad, surprise, neutral
batch_size = 256
epochs = 15


def train():
    with open("fer2013.csv") as f:
        content = f.readlines()

    lines = np.array(content)

    num_of_instances = lines.size
    print("number of instances: ", num_of_instances)
    print("instance length: ", len(lines[1].split(",")[1].split(" ")))
    # ------------------------------
    # initialize trainset and test set
    x_train, y_train, x_test, y_test = [], [], [], []

    # ------------------------------
    # transfer train and test set data
    for i in range(1, num_of_instances):
        try:
            emotion, img, usage = lines[i].split(",")

            val = img.split(" ")

            pixels = np.array(val, "float32")

            emotion = keras.utils.to_categorical(emotion, num_classes)

            if "Training" in usage:
                y_train.append(emotion)
                x_train.append(pixels)
            elif "PublicTest" in usage:
                y_test.append(emotion)
                x_test.append(pixels)
        except:
            print("", end="")

    # ------------------------------
    # data transformation for train and test sets
    x_train = np.array(x_train, "float32")
    y_train = np.array(y_train, "float32")
    x_test = np.array(x_test, "float32")
    y_test = np.array(y_test, "float32")

    x_train /= 255  # normalize inputs between [0, 1]
    x_test /= 255

    x_train = x_train.reshape(x_train.shape[0], 48, 48, 1)
    x_train = x_train.astype("float32")
    x_test = x_test.reshape(x_test.shape[0], 48, 48, 1)
    x_test = x_test.astype("float32")

    print(x_train.shape[0], "train samples")
    print(x_test.shape[0], "test samples")
    # ------------------------------
    # construct CNN structure
    model = Sequential()

    # 1st convolution layer
    model.add(Conv2D(64, (5, 5), activation="relu", input_shape=(48, 48, 1)))
    model.add(MaxPooling2D(pool_size=(5, 5), strides=(2, 2)))

    # 2nd convolution layer
    model.add(Conv2D(64, (3, 3), activation="relu"))
    model.add(Conv2D(64, (3, 3), activation="relu"))
    model.add(AveragePooling2D(pool_size=(3, 3), strides=(2, 2)))

    # 3rd convolution layer
    model.add(Conv2D(128, (3, 3), activation="relu"))
    model.add(Conv2D(128, (3, 3), activation="relu"))
    model.add(AveragePooling2D(pool_size=(3, 3), strides=(2, 2)))

    model.add(Flatten())

    # fully connected neural networks
    model.add(Dense(1024, activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(1024, activation="relu"))
    model.add(Dropout(0.2))

    model.add(Dense(num_classes, activation="softmax"))
    # ------------------------------
    # batch process
    gen = ImageDataGenerator()
    train_generator = gen.flow(x_train, y_train, batch_size=batch_size)

    # ------------------------------

    model.compile(
        loss="categorical_crossentropy",
        optimizer=keras2.optimizers.Adam(),
        metrics=["accuracy"],
    )

    # ------------------------------

    fit = True

    if fit == True:
        # model.fit_generator(x_train, y_train, epochs=epochs) #train for all trainset
        model.fit_generator(
            train_generator, steps_per_epoch=batch_size, epochs=epochs
        )  # train for randomly selected one
    else:
        model.load_weights("facial_expression_model_weights.h5")  # load weights

    # ------------------------------
    """
    #overall evaluation
    score = model.evaluate(x_test, y_test)
    print('Test loss:', score[0])
    print('Test accuracy:', 100*score[1])
    """
    model.save("facial_expression.keras")

train()

model = keras.models.load_model("facial_expression.keras")


def test(img):
    img = image.load_img(
        img, grayscale=True, target_size=(48, 48)
    )

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    x /= 255

    custom = model.predict(x)[0]
    # print(custom[0])
    exp = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
    for x, i in enumerate(custom):
        print(exp[x], ": ", i)

# test("temp/res.png")