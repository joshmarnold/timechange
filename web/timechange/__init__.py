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

import sys
import os
from os import path
import shutil
import numpy as np
import pandas
from PIL import Image
import timechange
# from .worker import *
from .train import *
from .model import *

#Keras includes


def new_project(project_path):
    """
    Create a new project
    """

    # delete current default directory
    if os.path.isdir(project_path):
        shutil.rmtree(project_path)

    # Create the project parent folder if necessary
    # folder will include:
    #   - /path/to/timechange
    #       - /csv
    #       - /images
    #       - /models
    #       - parameters.conf
    # If not, assume the project already exists
    if not path.exists(project_path):
        # New project
        os.makedirs(project_path)                      # makes multiple directories

        # Make project skeleton
        os.mkdir(path.join(project_path, "csv"))       # makes a directory project_path/csv
        os.mkdir(path.join(project_path, "images"))    # makes a directory project_path/images
        os.mkdir(path.join(project_path, "models"))    # makes a directory project_path/models

    else:
        # Existing project
        # Folder names and the file types within them
        folder_structure = {'csv':'csv', 'images':'png', 'models':'h5'}

        # Iterate over folder structure
        for folder_name, file_type in folder_structure.items():
            # Check if directory exists
            if path.exists(path.join(project_path, folder_name)):

                # Check if all files in that folder are csv files
                for label in os.scandir(path.join(project_path, folder_name)):
                    # So this works on 1 and 2-layer folders
                    try:
                        # Scan subdirectories
                        for entry in os.scandir(path.join(project_path, folder_name, label.name)):
                            # TODO: allow other extensions for ex: image
                            if not entry.name.endswith(file_type):
                                raise Exception("{} is not a {} file".format(
                                    path.join(project_path, folder_name, entry.name),
                                    file_type))
                    except NotADirectoryError:
                        # Scan subfiles
                        # TODO: allow other extensions for ex: image
                        if not label.name.endswith(file_type):
                            raise Exception("{} is not a {} file".format(
                                path.join(project_path, folder_name, label.name),
                                file_type))

            else:
                # directory does not exist
                raise Exception("{} cannot be a timechange project because {} does not exist".format(
                    project_path,
                    path.join(project_path, folder_name)))

        # Check for the config file
        if not path.exists(path.join(project_path, "parameters.conf")):
            raise Exception("{} cannot be a timechange project because {} does not exist".format(
                project_path,
                path.join(project_path, "parameters.conf")))


def add_training_file(label, file_path, project_path):
    """
    Adds a training file to the dataset under a specific label
    Keyword arguments:
    label -- the label to store the filename under
    filename -- the filename to add to the database
    """
    # If the folder for the label doesn't exist, create it
    if not path.exists(path.join(project_path, "csv", label)):
        os.mkdir(path.join(project_path, "csv", label))

    # Copy the csv file into the project
    # Uses the name of the original file.
    # TODO: generate better name
    shutil.copyfile(file_path, path.join(project_path, "csv", label, path.split(file_path)[1]))


def remove_training_file(project_path, label, filename):
    """
    Removes a training file from a label
    Keyword arguments:
    label -- the label to store the filename under
    filename -- the filename to add to the project
    """
    # Removes the file with the given name from the label's directory
    os.remove(path.join(project_path, "csv", label, filename))

    # Check to see if this was the last entry for a label
    if len(os.scandir(path.join(project_path, "csv", label))) == 0:
        # If this was the last entry, delete the label
        shutil.rmtree(path.join(project_path, "csv", label))


def get_csv_columns(project_path):
    """
    Reads a csv file and returns the column names
    """
    try:
        example_csv = os.scandir(os.scandir(path.join(project_path, "csv")).__next__().path).__next__().path
        return list(pandas.read_csv(example_csv, nrows=1).columns)
    except:
        return []


def get_csv_labels(project_path):
    """Returns a list of csv labels from the project tree."""
    return sorted([folder.name for folder in os.scandir(path.join(project_path, "csv"))])


def get_csv_filenames(project_path, label):
    """Returns a list of csv filenames for a specific label from the project tree."""
    return sorted([csv_file.name for csv_file in os.scandir(path.join(project_path, "csv", label))])
