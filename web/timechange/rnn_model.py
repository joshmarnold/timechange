import os
from os import path
#For creating images from numpy arrays
from PIL import Image
from keras.models import Sequential
from keras.layers import Convolution2D, ZeroPadding2D, MaxPooling2D
from keras.layers import Input, Dense, Flatten, Dropout
from keras.layers.recurrent import LSTM
from keras.layers.core import Reshape
from keras.optimizers import SGD
from keras.backend import common as K

def rnn_model(project_path, config):
    # Set dimension ordering
    K.set_image_dim_ordering('th')

    # Extract parameters from project folder
    image_folder = path.join(project_path, "images")

    # Extract number of classes from project by finding image folders
    num_classes = len(list(os.scandir(image_folder)))

    # Extract height and width of image
    image_height, image_width = Image.open(os.scandir(os.scandir(image_folder).__next__().path).__next__().path).size

    #Initialize a model object
    model = Sequential()

    # Extract and set parameters
    # Load number of blocks, with a default of 3
    num_blocks = config['num_blocks', 3]

    # Load a filter size list, with a default
    num_filters = config['num_filters']

    # Parse the filter list into useful values
    num_filters = [int(f) for f in num_filters.split(',')]

    # Extend the filter list to make sure it accounts for all blocks
    if len(num_filters) < num_blocks:
        # Pad the filter sizes with the last element
        num_filters.extend(num_filters[-1] * (num_blocks - len(num_filters)))

    # Extract the learning rate
    learning_rate = config['learning_rate']

    # Dynamically determine final layer's activation based
    # on the number of classes
    if num_classes == 2:
        final_activation = 'sigmoid'
        loss_measure = 'binary_crossentropy'
    else:
        final_activation = 'softmax'
        loss_measure = 'categorical_crossentropy'

    model.add(Reshape((image_height, image_width), input_shape=(1, image_height, image_width)))

    # Add the initial blocks
    # TODO: need to specify the output dimension
    model.add(LSTM(num_filters[0],
                   activation='relu',
                   return_sequences=True
                  ))

    # Add convolutional blocks. n-1 because the first was added already
    for layer in range(1, num_blocks - 1):
        # TODO: Allow configuring the parameters on these
        model.add(LSTM(num_filters[layer],
                  return_sequences = True))

    model.add(LSTM(num_filters[-1]))

    # TODO: Allow configuring the parameters and existence of these
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(num_classes, activation=final_activation))

    # Compile the model
    optimizer = SGD(lr=learning_rate)

    # Compile the model
    model.compile(loss=loss_measure,
                  optimizer=optimizer,
                  metrics=['accuracy'])

    return model