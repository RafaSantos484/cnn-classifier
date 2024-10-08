import os
from PIL import Image
import numpy as np
from tensorflow import keras

from params import img_size, color_mode
from .utils import zoom_img


def run():
    model = keras.models.load_model('tmp/model.keras')
    labels = os.listdir('imgs')
    filenames = []
    imgs_arrs = []
    for filename in os.listdir('predict_imgs'):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            img_path = f'predict_imgs/{filename}'
            filenames.append(filename)
            with Image.open(img_path) as img:
                img = img.convert(color_mode)
                img = img.resize((img_size, img_size))
                img = zoom_img(img)
                img_arr = np.array(img) / 255.
                imgs_arrs.append(img_arr)

    predictions = model.predict(np.array(imgs_arrs))
    for filename, prediction in zip(filenames, predictions):
        print(f'{filename}: {labels[np.argmax(prediction)]}')
