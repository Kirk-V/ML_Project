from keras.applications import VGG16
from keras.models import load_model
from numpy import loadtxt
import numpy as np
import cv2

# For loading pretrained model
# model = load_model('model.h5')
# summarize model
# model.summary()

# freezing last 4 layers of a keras model
for layers in vgg.layers:
    layer.trainable = False

vgg = VGG16(weights = 'imagenet',
            include_top = False,
            input_shape = (224, 224, 3))

# Gets the type of layer and if they're trainable
for (i, layer) in enumerate(vgg.layers):
    print(str(i) + " " + layer.__class__.__name__, layer.trainable)


from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, GlobalAveragePooling2D
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.layers.normalization import BatchNormalization
from keras.models import Model
from keras.optimizers import Adam
from keras.losses import SparseCategoricalCrossentropy
from keras.callbacks import ModelCheckpoint, EarlyStopping

dir = "."

AUTOTUNE = tf.data.experimental.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

## TODO get data from directory

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

model.compile(loss = losses.SparseCategoricalCrossentropy(from_logits=True),
                optimizer = 'adam', # may want something with learning rate
                metrics = ['accuracy'])

# amounts for train/test split per actor
num_train = 20
num_test = 20

# Training
epochs = 10
batch_size = 64