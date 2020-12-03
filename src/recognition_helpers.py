from keras.layers import Dense, Dropout, Activation, Flatten, GlobalAveragePooling2D
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D

def adapter(pre_trained_model, num_classes):
    """creates the top or head of the model that will be
    placed ontop of the bottom layers"""

    model = pre_trained_model.output
    model = Convolution2D(64, 3)(model)
    model = MaxPooling2D(pool_size=(2, 2))(model)
    model = Flatten()(model)
    model = Dense(1024,activation='relu')(model)     # May need more
    model = Dense(num_classes,activation='softmax')(model)
    return model