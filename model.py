# model.py
import tensorflow as tf
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from PIL import Image

model = tf.keras.models.load_model("plastic_classifier.h5")

def classify_image(image_path):
    img = Image.open(image_path).resize((224, 224))
    img_array = np.array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    preds = model.predict(img_array)
    label = "plastic" if preds[0][0] > 0.5 else "non-plastic"
    return label
