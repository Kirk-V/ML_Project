import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import VGG16

gpu_options = tf.compat.v1.GPUOptions(allow_growth=True)
session = tf.compat.v1.InteractiveSession(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))

batch_size = 16
img_height = 224
img_width = 224

vgg = VGG16(weights = 'imagenet',
            include_top = False,
            # input_tensor=tf.keras.Input(shape=(img_height, img_width, 3)),
            # pooling = 'max',
            input_shape = (img_height, img_width, 3))

# freezing last 4 layers of a keras model
for layer in vgg.layers:
    layer.trainable = False

# Gets the type of layer and if they're trainable
for (i, layer) in enumerate(vgg.layers):
    print(str(i) + " " + layer.__class__.__name__, layer.trainable)


from tensorflow.keras import layers
from tensorflow.keras.models import Model

data_dir = "../DataSetToSend/"

train_samples = 40
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.25,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size)

val_samples = 10
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.25,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size)

class_names = train_ds.class_names
print(class_names)

# Caches data between runs
# AUTOTUNE = tf.data.experimental.AUTOTUNE
# train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
# val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# # Normalizes input for performance
normalization_layer = layers.experimental.preprocessing.Rescaling(1./255)
# model = Model(inputs = normalization_layer, outputs = vgg)

norm_train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
norm_val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))
# # image_batch, labels_batch = next(iter(normalized_ds))
# # first_image = image_batch[0]
# # Notice the pixels values are now in `[0,1]`.
# # print(np.min(first_image), np.max(first_image))

from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, GlobalAveragePooling2D
from tensorflow.keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.optimizers import RMSprop
import recognition_helpers as rf

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

## Training
epochs = 10
batch_size = 16
num_classes = 5

# adapter = rf.adapter(vgg, num_classes)
# # model = Model(inputs = vgg.input, outputs = adapter)
# x = vgg.get_layer('block5_pool').output
# # Stacking a new simple convolutional network on top of it
# x = Conv2D(64, 3)(x)
# x = MaxPooling2D(pool_size=(2, 2))(x)
# x = Flatten()(x)
# x = Dense(num_classes, activation='relu')(x)
# x = Dense(num_classes, activation='softmax')(x)

top_model = vgg.output
top_model = GlobalAveragePooling2D()(top_model)
top_model = Dense(1024,activation='relu')(top_model)
top_model = Dense(1024,activation='relu')(top_model)
top_model = Dense(512,activation='relu')(top_model)
top_model = Dense(num_classes,activation='softmax')(top_model)

model = Model(inputs=vgg.input, outputs=top_model)

# opt = tf.keras.optimizers.Adam(learning_rate=0.001)
# model.compile(loss = tf.keras.losses.binary_crossentropy,
#               optimizer = opt,
#               metrics = ['accuracy'])

model.compile(loss = 'categorical_crossentropy',
              optimizer = RMSprop(lr = 0.001),
              metrics = ['accuracy'])

history = model.fit(
    train_ds,
    validation_data = val_ds,
    # steps_per_epoch = train_samples // batch_size,
    epochs = epochs)
    # callbacks = callbacks,
    # validation_steps = val_samples // batch_size)


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
