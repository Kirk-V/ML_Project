import cv2
import tensorflow as tf
from keras.models import load_model

gpu_options = tf.compat.v1.GPUOptions(allow_growth=True)
session = tf.compat.v1.InteractiveSession(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))


classifier = load_model('face_vgg.h5')

# for i in range(0,10):
input_im = cv2.imread("./detectedImages/0220px-JayBaruchel08TIFF.jpg")

# cv2.imshow('image', input_im)
input_original = input_im.copy()
input_original = cv2.resize(input_original, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_LINEAR)

input_im = cv2.resize(input_im, (224, 224), 3, interpolation = cv2.INTER_LINEAR)
input_im = input_im / 255.
input_im = input_im.reshape(1,224,224,3)

# Get Prediction
res = classifier.predict(input_im, 1, verbose = 0)

## TODO
# Learn how to get classes
# Learn how to hook this up to detected face/Kirk model
# Learn how this connects to front end

print(res)