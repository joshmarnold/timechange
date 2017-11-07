from os import path
from configparser import ConfigParser
from conv_model import *
from rnn_model import *
#For creating images from numpy arrays

# from PIL import Image
# from keras.models import Sequential
# from keras.layers import Convolution2D, ZeroPadding2D, MaxPooling2D
# from keras.layers import Input, Dense, Flatten, Dropout
# from keras.optimizers import SGD
# from keras.backend import common as K

def build_model(project_path):
    """Generates a compiled keras model for use in timechange training
    Parameters: 
    project_path -- path to a timechange project"""

    # Extract configuration
    config = ConfigParser()
    config.read(path.join(project_path,'parameters.conf'))
    
    #Extract model type from configuration
    model_type = config['DEFAULT'].get('model_type', 'convolutional_basic').strip('\"').strip('\'')
    
    #Determine the model type
    if model_type == 'convolutional_basic':
        model = conv_model(project_path, config)
    elif model_type == 'rnn_basic':
        model = rnn_model(project_path, config)
    else:
        raise Exception("Invalid neural net type")

    #Output the model
    return model
