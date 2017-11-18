from web import settings
from web import app
from flask import render_template, redirect, flash, url_for, request
from flask_restful import reqparse
from . import *
from .transform import *

PROJECT_PATH = path.join(path.dirname(path.abspath(__file__)), '../default/')
app.config['PROJECT_PATH'] = PROJECT_PATH

@app.route('/transform_data_timechange', methods=['POST'])
def transform_data_timechange():
    """
    Iterates over the training files set and generates corresponding images
    using the feature extraction method

    Keyword arguments:
    project path -- path to project data (kept as a global in flask)
    method       -- Method used by extract_features to generate image data. Default: fft
    chunk_size   -- number of timesteps to include in each fft
    fft_size     -- size of the fft
    columns      -- comma separated string of columns to use
    """

    parser = reqparse.RequestParser()
    parser.add_argument('options', type=str, required=True)
    parser.add_argument('chunk_size', type=int, required=True)
    parser.add_argument('fft_size', type=int, required=True)
    parser.add_argument('columns', required=True)
    args = parser.parse_args()

    convert_all_csv(PROJECT_PATH, args['options'], args['fft_size'], args['chunk_size'], args['columns'])
    return (''), 204


@app.route('/configure_timechange', methods=['POST'])
def configure_timechange():
    """
    Generates a compiled keras model for use in timechange training
    Parameters:
    project_path -- path to a timechange project
    config -- dict containing configuration setting (model_type, num_block, num_filters, learning_rate)
    """
    pars = reqparse.RequestParser(bundle_errors=True)
    pars.add_argument('model_type', required=True)
    pars.add_argument('num_block', type=int, required=True)
    pars.add_argument('num_filters', type=str, required=True)
    pars.add_argument('learning_rate', type=float, required=True)
    args = pars.parse_args()

    build_model(PROJECT_PATH, args)
    return (''), 204

@app.route('/train_timechange', methods=['POST'])
def train_timechange():
    """
    Generates a compiled keras model for use in timechange training
    Parameters:
    project_path -- path to a timechange project
    config -- dict containing configuration setting (model_type, num_block, num_filters, learning_rate)
    """
    print("IN Train")

    ret = train(PROJECT_PATH)
    print(ret)

    return (''), 204












# space
