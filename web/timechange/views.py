from web import settings
from web import app
from flask import render_template, redirect, flash, url_for, request
from flask_restful import reqparse
from . import *


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

    print("in transform")

    # parser = reqparse.RequestParser()
    # parser.add_argument('chunk_size', type=int, required=True, help='Forgot to add chunk size')
    # parser.add_argument('name')
    # args = parser.parse_args()
    #
    # convert_all_csv(PROJECT_PATH, trans_type, chunk_size, fft_size, columns)
    return (''), 204


#
# @app.route('/transform_data_timechange', methods=['POST'])
# def transform_data_timechange():
#     """
#     Iterates over the training files set and generates corresponding images
#     using the feature extraction method
#
#     Keyword arguments:
#     project path    -- path to project data (kept as a global in flask)
#     method          -- Method used by extract_features to generate image data. Default: fft
#     chunk_size      -- number of timesteps to include in each fft
#     fft_size        -- size of the fft
#     columns         -- comma separated string of columns to use
#     """
#
#     convert_all_csv(PROJECT_PATH), trans_type, chunk_size, fft_size, columns)
#     return (''), 204
#
# @app.route('/transform_data_timechange', methods=['POST'])
# def transform_data_timechange():
#     """
#     Iterates over the training files set and generates corresponding images
#     using the feature extraction method
#
#     Keyword arguments:
#     project path    -- path to project data (kept as a global in flask)
#     method          -- Method used by extract_features to generate image data. Default: fft
#     chunk_size      -- number of timesteps to include in each fft
#     fft_size        -- size of the fft
#     columns         -- comma separated string of columns to use
#     """
#     convert_all_csv(os.path.join(PROJECT_PATH, "csv/labels/"), trans_type, chunk_size, fft_size, columns)
#     return (''), 204
