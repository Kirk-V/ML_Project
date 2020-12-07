import tensorflow as tf
from tensorflow.keras.applications import VGG16, ResNet50V2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import RMSprop, Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

## Set up and making network

# Sets GPU options for automatic memory allocation. Mandatory
gpu_options = tf.compat.v1.GPUOptions(allow_growth=True)
session = tf.compat.v1.InteractiveSession(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))

# VGG was designed to work on 224 x 224 pixel input images sizes
# Classes is the same as the number of actors you use
im_height, im_width = 224, 224
num_classes = 6

# Loads VGG trained on imagenet without the top layer
vgg = ResNet50V2(weights = 'imagenet', 
                 include_top = False, 
                 input_shape = (im_height, im_width, 3))

# Freeze the VGG layers
for layer in vgg.layers:
    layer.trainable = False

# The new layers to add to VGG
adapter = vgg.output
adapter = GlobalAveragePooling2D()(adapter)
adapter = Dense(1024, activation='relu')(adapter)
adapter = Dense(1024, activation='relu')(adapter)
adapter = Dense(512, activation='relu')(adapter)
adapter = Dense(num_classes, activation='softmax')(adapter)

model = Model(inputs = vgg.input, outputs = adapter)
# print(model.summary())

# # Prints layers
# for (i,layer) in enumerate(vgg.layers):
#     print(str(i) + " "+ layer.__class__.__name__, layer.trainable)


## Loading datasets

image_dir = "./DataSetToSend/"

# Augments the data to create more permutations to train over
#   Rotation rotates the image 45 degrees to each side
#   Shifts of size 0.2 move the the images randomly 20% of the whole size up, down, left or right
#   Can zoom up to 60%
#   Nearest neighbor scaling
#   May flip horizontally (like a mirror)
#   Rescale is rescaling factor
#   Validation split is 80% training, 20% validation
train_datagen = ImageDataGenerator(
    rotation_range=45,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.6,
    fill_mode='nearest',
    horizontal_flip=True,
    rescale=1./255,
    validation_split=0.2)

# Batch size to load
batch_size = 32

# Generators infer labels from class mode and get class mode. Categorical as we are finding actors
#   Seed is to have consistency for random elements
#   Bilinear interpologation to get image to 224 x 224
train_generator = train_datagen.flow_from_directory(
    image_dir,
    class_mode='categorical',
    target_size=(im_height, im_width),
    batch_size=batch_size,
    seed=42,
    subset="training",
    interpolation='bilinear')

val_generator = train_datagen.flow_from_directory(
    image_dir,
    class_mode='categorical',
    target_size=(im_height, im_width),
    batch_size=batch_size,
    seed=42,
    subset="validation",
    interpolation='bilinear')

# Check pointing to save best weights and to stop early if loss is not improving
#   Attempts to keep the minimum validation loss. Some verbosity to watch training
model_checkpoint = ModelCheckpoint(
    "resnet_weights.h5",
    monitor="val_loss",
    verbose=1,
    save_best_only = True,
    mode="min",
    )

# Same principle as above, patience is 4 epochs with no changes
early_stopping = EarlyStopping(
    monitor = 'val_loss',
    patience = 4,
    verbose = 1,
    restore_best_weights = True)

# Has to be categorical cross-entropy as people are discrete
#   Simply train on accuracy. RMSProp can be useful for image classification, watches moving average of SGD
model.compile(loss = 'categorical_crossentropy', 
              optimizer = RMSprop(lr = 0.001),
              metrics = ['accuracy'])



## Training and fine-tuning
# Train 30 epochs before fine tuning
epochs = 30
batch_size = 64
history = model.fit(
    train_generator,
    epochs = epochs,
    callbacks = [early_stopping, model_checkpoint],
    validation_data = val_generator)

# Fine-Tune by setting base model trainiable. Use adaptive loss
vgg.trainable = True
adam = Adam(learning_rate=0.0001)

# Recompile model tp fine-tune
model.compile(loss = 'categorical_crossentropy',
              optimizer = adam,
              metrics = ['accuracy'])

# Tune for 40 epochs now
fine_tune_epochs = 10
total_epochs = fine_tune_epochs + epochs
model.summary()

history_fine = model.fit(
    train_generator,
    epochs=total_epochs,
    initial_epoch = history.epoch[-1],
    validation_data=val_generator)

epochs_range = range(epochs)

model.save('resnet_weights.h5')
history = history_fine



## Visualizing accuracy and loss - pulled from Keras tutorial
import matplotlib.pyplot as plt
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

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
