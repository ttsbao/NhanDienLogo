from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import numpy as np


np.set_printoptions(suppress=True)

model = load_model('D:/Project/MachineLearning/NhanDienLogo/keras_model.h5')

print(model.summary())

#photo_filename = 'D:/Project/MachineLearning/NhanDienLogo/003.png'

input_w, input_h = 224, 224

# image, image_w, image_h = load_image_pixels(photo_filename, (input_w, input_h))
#
# yhat = model.predict(image)

data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


image = Image.open('D:/Project/MachineLearning/NhanDienLogo/003.png')

size = (224, 224)
image = image.resize((224, 224))

image = ImageOps.fit(image, size, Image.ANTIALIAS)

#print(image)

image_array = np.asarray(image)

#image.show()

normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

data[0] = normalized_image_array

yhat = model.predict(data)

print(yhat)



