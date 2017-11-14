from .conv_model import *
from .rnn_model import *
import keras


def build_model(project_path, config):
    """
    Generates a compiled keras model for use in timechange training
    Parameters:
    project_path -- path to a timechange project
    config -- dict containing configuration setting (model_type, num_blocks, num_filters, learning_rate)
    """

    # Extract model type from configuration
    model_type = config['model_type']

    # Determine the model type
    if model_type == 'convolutional':
        model = conv_model(project_path, config)
    elif model_type == 'rnn':
        model = rnn_model(project_path, config)
    else:
        raise Exception("Invalid neural net type")

    # Output the model
    model.save(path.join(project_path, "models", "latest.h5"))

