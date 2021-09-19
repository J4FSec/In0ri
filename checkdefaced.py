import numpy as np
import tensorflow as tf
from tensorflow import keras

img_height = 250
img_width = 250
model = keras.models.load_model("/opt/In0ri/final_model.h5")


def check(images_path):
    img = keras.preprocessing.image.load_img(
        images_path, target_size=(img_height, img_width)
    )
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    class_names = ["clean", "defaced"]
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[-1])
    if format(class_names[np.argmax(score)]) == "defaced":
        return 1
    else:
        return 0
