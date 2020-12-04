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
            input_shape = (img_height, img_width, 3))

# freezing last 4 layers of a keras model
for layer in vgg.layers:
    layer.trainable = False

# Gets the type of layer and if they're trainable
for (i, layer) in enumerate(vgg.layers):
    print(str(i) + " " + layer.__class__.__name__, layer.trainable)


from tensorflow.keras import layers

data_dir = "../part1/dir_001/Aaron Paul"

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
AUTOTUNE = tf.data.experimental.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# # Normalizes input for performance
normalization_layer = layers.experimental.preprocessing.Rescaling(1./255)

normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
# image_batch, labels_batch = next(iter(normalized_ds))
# first_image = image_batch[0]
# Notice the pixels values are now in `[0,1]`.
# print(np.min(first_image), np.max(first_image))


from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.models import Model
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
batch_size = 64
num_classes = 100

adapter = rf.adapter(vgg, num_classes)
model = Model(inputs = vgg.input, outputs = adapter)
model.compile(loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              optimizer = 'adam', # may want something with learning rate
              metrics = ['accuracy'])

history = model.fit(
    normalized_ds,
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