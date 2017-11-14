import keras
from keras.backend import common as K
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from PIL import Image
import os
from os import path


def train(project_path):
    """
    Trains a neural net model on the project's data set

    Parameters:
    project_path -- path to project's data (stored as global in flask)
    """

    # load the compiled model
    model = load_model(path.join(project_path, "models", "latest.h5"))

    # Set dimension ordering
    K.set_image_dim_ordering('th')

    # Load the image size
    image_size = Image.open(os.scandir(os.scandir(path.join(project_path, "images")).__next__().path).__next__().path).size

    # Check to see if a model has been generated
    if model is None:
        raise Exception("There is no model stored. Please generate a model before training")

    # Determine class mode based on folder structure
    num_classes = len(list(os.scandir(path.join(project_path, "images"))))
    if num_classes == 1:
        raise Exception("The training data only contains one class")
    else:
        class_mode = "categorical"

    # Create a training data generator from the images folder
    train_generator = ImageDataGenerator(
            rescale=1.0/255.0,  # Scale the 0-255 pixel values down to 0.0-1.0
            dim_ordering='th'  # samples, channels, width, height
            ).flow_from_directory(
            path.join(project_path, 'images'),  # Read training data from the project's images dir
            target_size=image_size,  # Resize must be set or the generator will automatically choose dimensions
            color_mode='grayscale',  # TODO: take another look at this
            batch_size=64,  # TODO: customize this
            shuffle=True,  # Shuffle the data inputs. TODO: set a random seed
            class_mode=class_mode)  # TODO: consider binary mode for systems with only 2 labels

    # Design a callback to store training progress
    class ProgressBarCallback(keras.callbacks.Callback):
        def on_train_begin(self, logs={}):
            return

        def on_train_end(self, logs={}):
            return

        def on_epoch_begin(self, epoch, logs={}):
            return

        def on_epoch_end(self, epoch, logs={}):
            print("Training epoch {} ended".format(epoch))
            return

        def on_batch_begin(self, batch, logs={}):
            return

    model.save_weights(path.join(project_path, "models", "latest.h5"))

    # Train the model
    # TODO: k-fold validation
    try:
        return model.fit_generator(
            train_generator,
            samples_per_epoch=len(train_generator.filenames),  # TODO: better solution
            nb_epoch=20,
            callbacks=[ProgressBarCallback()]).history  # TODO: customize this
    except Exception as err:
        # TODO: Handle error better
        raise Exception("Something went wrong with the training process: {}".format(str(err)))
