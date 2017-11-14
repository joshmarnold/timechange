#!/usr/bin/env python3

"""Copyright 2017
Steven Sheffey <stevensheffey4@gmail.com>,
John Ford,
Eyasu Asrat,
Jordan Flowers,
Joseph Volmer,
Luke Stanley,
Serenah Smith, and
Chandu Budati

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from collections import defaultdict
from queue import Queue
from threading import Thread
import sys, os.path
import os
from os import path
import shutil
from configparser import ConfigParser
import numpy as np
import pandas
from PIL import Image
import timechange
from .worker import *
from .train import *
from .model import *

#Keras includes

#Default parameter config file. Included here due to tab issues
default_parameter_config = """[DEFAULT]
#The type of neural net to generate
#Settings for the chosen type will be stored under a
#section of the same name
model_type = convolutional_basic

[convolutional_basic]
#The number of convolutional blocks to use for the model
num_blocks = 3

#The number of filters for these blocks (comma-separated list)
#If the size of this list is less than num_blocks, the last value
#will be used for the remaining values

num_filters = 16,8,8

[rnn_basic]
#The number of rnn blocks to use for the model
num_blocks = 3

#The number of filters for these blocks (comma-separated list)
#If the size of this list is less than num_blocks, the last value
#will be used for the remaining values

num_filters = 16, 8, 8

#Learning rate for training
learning_rate = 1e-2
"""
#Default transform config file. Included here due to tab issues
default_transform_config = """[DEFAULT]
#CSV columns to read
columns=
#Type of transform to run
method=fft
#Size of the chunks
chunk_size=64
#Size of the fft output
fft_size=128
"""

def new_project(project_path):
    """
    Create a new project
    """

    # delete current default directory
    if os.path.isdir(project_path):
        shutil.rmtree(project_path)

    #Stores where the project profile will be kept
    # create path with parent directory and projectname
    # project_path = path.abspath(path.join(parent_folder, project_name))
    print(project_path)

    #Create the project parent folder if necessary
    #folder will include:
    #   - /path/to/timechange
    #       - /csv
    #       - /images
    #       - /models
    #       - parameters.conf
    #If not, assume the project already exists
    if not path.exists(project_path):
        #New project
        os.makedirs(project_path)                      # makes multiple directories

        #Make project skeleton
        os.mkdir(path.join(project_path, "csv"))       # makes a directory project_path/csv
        os.mkdir(path.join(project_path, "images"))    # makes a directory project_path/images
        os.mkdir(path.join(project_path, "models"))    # makes a directory project_path/models

        #Create a parameters file
        # first line creates a file, config_file, in path project_path/parameters.conf
        with open(path.join(project_path, "parameters.conf"), "w") as config_file:
            config_file.write(default_parameter_config)

        #Create a transform file -- same procedure as above
        with open(path.join(project_path, "transform.conf"), "w") as config_file:
            config_file.write(default_transform_config)

    else:
        #Existing project
        #Folder names and the file types within them
        folder_structure = {'csv':'csv', 'images':'png', 'models':'h5'}

        #Iterate over folder structure
        for folder_name, file_type in folder_structure.items():
            #Check if directory exists
            if path.exists(path.join(project_path, folder_name)):

                #Check if all files in that folder are csv files
                for label in os.scandir(path.join(project_path, folder_name)):
                    #So this works on 1 and 2-layer folders
                    try:
                        #Scan subdirectories
                        for entry in os.scandir(path.join(project_path, folder_name, label.name)):
                            #TODO: allow other extensions for ex: image
                            if not entry.name.endswith(file_type):
                                raise Exception("{} is not a {} file".format(
                                    path.join(project_path, folder_name, entry.name),
                                    file_type))
                    except NotADirectoryError:
                        #Scan subfiles
                        #TODO: allow other extensions for ex: image
                        if not label.name.endswith(file_type):
                            raise Exception("{} is not a {} file".format(
                                path.join(project_path, folder_name, label.name),
                                file_type))

            else:
                #directory does not exist
                raise Exception("{} cannot be a timechange project because {} does not exist".format(
                    project_path,
                    path.join(project_path, folder_name)))

        #Check for the config file
        if not path.exists(path.join(project_path, "parameters.conf")):
            raise Exception("{} cannot be a timechange project because {} does not exist".format(
                project_path,
                path.join(project_path, "parameters.conf")))


def add_training_file(label, file_path, project_path):
    """Adds a training file to the dataset under a specific label
    Keyword arguments:
    label -- the label to store the filename under
    filename -- the filename to add to the database
    """
    #If the folder for the label doesn't exist, create it
    if not path.exists(path.join(project_path, "csv", label)):
        os.mkdir(path.join(project_path, "csv", label))

    #Copy the csv file into the project
    #Uses the name of the original file.
    #TODO: generate better name
    shutil.copyfile(file_path, path.join(project_path, "csv", label, path.split(file_path)[1]))

def remove_training_file(self, label, filename):
    """Removes a training file from a label
    Keyword arguments:
    label -- the label to store the filename under
    filename -- the filename to add to the project
    """
    #Removes the file with the given name from the label's directory
    os.remove(file_path, path.join(self.project_path, "csv", label, path.split(file_path)[1]))

    #Check to see if this was the last entry for a label
    if len(os.scandir(path.join(self.project_path, "csv", label))) == 0:
        #If this was the last entry, delete the label
        shutil.rmtree(path.join(self.project_path, "csv", label))

def set_columns(self, columns):
    """Sets the CSV columns to be used by the transform process"""
    #Load the config for transform parameters
    transform_config = ConfigParser()
    transform_config.read(path.join(self.project_path, "transform.conf"))
    transform_config["DEFAULT"]["columns"] = ",".join(map(str, columns))

    with open(path.join(self.project_path, "transform.conf"), "w") as transform_config_file:
        transform_config.write(transform_config_file)

def set_transform_parameters(self, **kwargs):
    """Writes transform parameters to the transform configuration"""
    #Load the config for transform parameters
    transform_config = ConfigParser()
    transform_config.read(path.join(self.project_path, "transform.conf"))

    for parameter, value in kwargs.items():
        transform_config["DEFAULT"][parameter] = value

    with open(path.join(self.project_path, "transform.conf"), "w") as transform_config_file:
        transform_config.write(transform_config_file)

def get_transform_parameters(self):
    """Gets the transform parameters"""
    #Load the config for transform parameters
    transform_config = ConfigParser()
    transform_config.read(path.join(self.project_path, "transform.conf"))
    return transform_config["DEFAULT"]

def get_csv_columns(self):
    """Reads a csv file and returns the column names
    """
    try:
        example_csv = os.scandir(os.scandir(path.join(self.project_path, "csv")).__next__().path).__next__().path
        return list(pandas.read_csv(example_csv, nrows=1).columns)
    except:
        return []

def get_csv_labels(self):
    """Returns a list of csv labels from the project tree."""
    return sorted([folder.name for folder in os.scandir(path.join(self.project_path, "csv"))])

def get_csv_filenames(self, label):
    """Returns a list of csv filenames for a specific label from the project tree."""
    return sorted([csv_file.name for csv_file in os.scandir(path.join(self.project_path, "csv", label))])