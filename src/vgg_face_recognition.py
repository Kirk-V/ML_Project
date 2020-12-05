# -*- coding: utf-8 -*-
"""vgg_face_recognition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/155DpJ_756FDztY5s6OX5EYBAKWyq9lXV
"""
import tensorflow as tf
from tensorflow.keras.applications import VGG16

gpu_options = tf.compat.v1.GPUOptions(allow_growth=True)
session = tf.compat.v1.InteractiveSession(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))

# VGG was designed to work on 224 x 224 pixel input images sizes
img_rows, img_cols = 224, 224 

# Re-loads the VGG model without the top or FC layers
vgg = VGG16(weights = 'imagenet', 
                 include_top = False, 
                 input_shape = (img_rows, img_cols, 3))

# Here we freeze the last 4 layers 
# Layers are set to trainable as True by default
for layer in vgg.layers:
    layer.trainable = False
    
# Let's print our layers 
for (i,layer) in enumerate(vgg.layers):
    print(str(i) + " "+ layer.__class__.__name__, layer.trainable)

def Fc(bottom_model, num_classes):
    """creates the top or head of the model that will be 
    placed ontop of the bottom layers"""

    top_model = bottom_model.output
    top_model = GlobalAveragePooling2D()(top_model)
    top_model = Dense(1024,activation='relu')(top_model)
    top_model = Dense(1024,activation='relu')(top_model)
    top_model = Dense(512,activation='relu')(top_model)
    top_model = Dense(num_classes,activation='softmax')(top_model)
    return top_model

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, GlobalAveragePooling2D
from tensorflow.keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from tensorflow.keras.models import Model

# Set our class number to 3 (Young, Middle, Old)
num_classes = 5

FC_Head = Fc(vgg, num_classes)

model = Model(inputs = vgg.input, outputs = FC_Head)

print(model.summary())

from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_data_dir = "../DataSetToSend/"
# validation_data_dir = '/content/drive/My Drive/image_dataset/validate/'

# Let's use some data augmentaiton 
train_datagen = ImageDataGenerator(
      validation_split=0.2,
      rescale=1./255,
      rotation_range=45,
      width_shift_range=0.3,
      height_shift_range=0.3,
      horizontal_flip=True,
      fill_mode='nearest')
 
validation_datagen = ImageDataGenerator(rescale=1./255)
 
# set our batch size (typically on most mid tier systems we'll use 16-32)
batch_size = 32
 
train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        subset="training",
        target_size=(img_rows, img_cols),
        batch_size=batch_size,
        class_mode='categorical')
 
validation_generator = train_datagen.flow_from_directory(
        train_data_dir,
        subset="validation",
        target_size=(img_rows, img_cols),
        batch_size=batch_size,
        class_mode='categorical')

from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
checkpoint = ModelCheckpoint("face_vgg.h5",
                             monitor="val_loss",
                             mode="min",
                             save_best_only = True,
                             verbose=1)

earlystop = EarlyStopping(monitor = 'val_loss', 
                          min_delta = 0, 
                          patience = 3,
                          verbose = 1,
                          restore_best_weights = True)

# we put our call backs into a callback list
callbacks = [earlystop, checkpoint]
# We use a very small learning rate 
model.compile(loss = 'categorical_crossentropy',
              optimizer = RMSprop(lr = 0.001),
              metrics = ['accuracy'])
# Enter the number of training and validation samples here
nb_train_samples = 200
nb_validation_samples = 200
# We only train 5 EPOCHS 
epochs = 10
batch_size = 64
history = model.fit_generator(
    train_generator,
    # steps_per_epoch = nb_train_samples // batch_size,
    epochs = epochs,
    callbacks = callbacks,
    validation_data = validation_generator)
    # validation_steps = nb_validation_samples // batch_size)

## Visualizing results
import matplotlib.pyplot as plt
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

# from keras.models import load_model
#
# classifier = load_model('face_vgg.h5')
#
# from collections import defaultdict
#
# d = defaultdict(list)
# d[0].append(1)

# import os
# import cv2
# import numpy as np
# from os import listdir
# from google.colab.patches import cv2_imshow
# from os.path import isfile, join
#
# set1_dict = { "[0]": "mansi_mummy",
#               "[1]": "mansi"
#              }
#
# set1_dict_n = { "n0": "mansi_mummy",
#                 "n1": "mansi"
#               }
#
# def draw_test(name, pred, im):
#     man = set1_dict[str(pred)]
#     BLACK = [0,0,0]
#     expanded_image = cv2.copyMakeBorder(im, 80, 0, 0, 100 ,cv2.BORDER_CONSTANT,value=BLACK)
#     cv2.putText(expanded_image, man, (20, 60) , cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,255), 2)
#     cv2_imshow(expanded_image)
#
# def getRandomImage(path):
#     """function loads a random images from a random folder in our test path """
#     folders = list(filter(lambda x: os.path.isdir(os.path.join(path, x)), os.listdir(path)))
#     random_directory = np.random.randint(0,len(folders))
#     path_class = folders[random_directory]
#     print("Class - " + set1_dict_n[str(path_class)])
#     file_path = path + path_class
#     file_names = [f for f in listdir(file_path) if isfile(join(file_path, f))]
#     random_file_index = np.random.randint(0,len(file_names))
#     image_name = file_names[random_file_index]
#     return cv2.imread(file_path+"/"+image_name)
#
#
# for i in range(0,10):
#     input_im = getRandomImage("/content/drive/My Drive/image_dataset/train/")
#     input_original = input_im.copy()
#     input_original = cv2.resize(input_original, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_LINEAR)
#
#     input_im = cv2.resize(input_im, (224, 224), interpolation = cv2.INTER_LINEAR)
#     input_im = input_im / 255.
#     input_im = input_im.reshape(1,224,224,3)
#
#     # Get Prediction
#     res = np.argmax(classifier.predict(input_im, 1, verbose = 0), axis=1)
#
#     # Show image with predicted class
#     draw_test("Prediction", res, input_original)
#     cv2.waitKey(0)
#
#
# cv2.destroyAllWindows()
#
#



