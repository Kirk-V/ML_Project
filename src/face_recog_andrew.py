from keras.applications import VGG16
from keras.models import load_model
from numpy import loadtxt
import numpy as np
import cv2

# For loading pretrained model
# model = load_model('model.h5')
# summarize model.
# model.summary()

# freezing last 4 layers of a keras model
# for layers in vgg.layers:
#     layer.trainable = False

img_rows, img_cols = 244, 2444
vgg = VGG16(weights = 'imagenet',
            include_top = False,
            input_shape = (img_rows, img_cols, 3))

# Gets the ype of layer and if they're trainable
for (i, layer) in enumerate(vgg.layers):
    print(str(i) + " " + layer.__class__.__name__, layer.trainable)

# from keras.models import Sequential
# from keras.layers import Dense, Dropout, Activation, Flatten, GlobalAveragePooling2D
# from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
# from keras.layers.normalization import BatchNormalization
# from keras.models import Model