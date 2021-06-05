import tensorflow as tf
import numpy as np
from keras_preprocessing import image
from werkzeug.utils import secure_filename
from tensorflow.keras.applications.xception import preprocess_input



model = tf.keras.models.load_model(filepath="./prediction/model_inceptionv3.h5")

def model_predict(images):
    img = image.load_img(images, target_size=(224, 224, 3))

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    images = np.vstack([x])
    prediction = model.predict(images, batch_size=32)

    return prediction