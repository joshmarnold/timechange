#For reading config files
from configparser import ConfigParser
#For navigating filesystems
import os
from os import path
#For deleting directories
import shutil
#For padding data
import numpy as np
#For creating images from numpy arrays
from PIL import Image
#For reading csv files
import pandas
#For performing transformations
from . import transform
from . import model
from . import train

def convert_all_csv(project_path):
    """Iterates over the training files set and generates corresponding images
    using the feature extraction method
    Keyword arguments:
    method -- Method used by extract_features to generate image data. Default: fft"""

    # Extract parameters from project path
    transform_config = ConfigParser()
    transform_config.read(path.join(project_path, "transform.conf"))

    #Columns to read from the csv
    columns = transform_config["DEFAULT"].get("columns", "").split(",")

    #Default to reading all columns if this fails
    if columns == [""]:
        columns = None

    #Type of transformation to apply
    method = transform_config["DEFAULT"].get("method", "fft").strip("\"").strip("\'")

    #Size of chunks
    chunk_size = int(transform_config["DEFAULT"].get("chunk_size", "64").strip("\"").strip("\'"))

    #Size of fft output
    fft_size = int(transform_config["DEFAULT"].get("fft_size", "128").strip("\"").strip("\'"))

    #Clear subfolders in image folder without deleting images folder
    #This is to make sure old images don't stick around
    #In case a file has been removed
    for label in os.scandir(path.join(project_path, "images")):
        #Delete the folder
        try:
            shutil.rmtree(label.path)
        except FileNotFoundError as _:
            #Do nothing
            pass

    #Get length of longest csv file
    max_length = -1

    #Iterate over labels
    for label in os.scandir(path.join(project_path, "csv")):

        #Iterate over a label's csv files
        for csv_file in os.scandir(label.path):
            with open(csv_file.path, 'r') as csv_file_handle:
                #Get number of lines in file and keep track of longest file
                max_length = max(max_length, len(csv_file_handle.readlines()) - 1)

    #Generate new images
    #Iterate over labels
    for label in os.scandir(path.join(project_path, "csv")):
        #Make a folder for the label
        os.mkdir(path.join(project_path, "images", label.name))

        #Iterate over a label's csv files
        for csv_file in os.scandir(label.path):
            # Read the csv into a numpy array
            data = pandas.read_csv(csv_file.path, usecols=columns).as_matrix().T

            # Pad the csv
            data = np.pad(data, ((0,0), (0, max_length - data.shape[1])), 'constant', constant_values=0.0)

            # Extract features from the numpy array
            # Uses same variable name since data is not needed after feature extraction
            data = transform.extract(data, method, chunk_size=chunk_size, fft_size=fft_size)

            # TODO: normalize and imageize here
            # TODO: Don't imagize at all
            # Generate an image from the resulting feature representation
            img = Image.fromarray((data * 255).astype(np.uint8), "RGB")

            # Save the image to the desired file path
            # project/csv/example/1.csv becomes
            # project/images/example/1.png
            img.save(path.join(project_path, "images", label.name, "{}.png".format(path.splitext(csv_file.name)[0])))


def worker_thread(project_path, input_queue, output_queue):
    #Import keras immediately to get it set up
    import keras
    try:
        model = generate_model(project_path)
    except:
        model = None
    while True:
        job = input_queue.get()

        #Transform the data
        if job["command"] == "transform":
            #Attempt to transform data
            try:
                #Run the conversion process
                convert_all_csv(project_path)
                #Inform the main thread that transformation is finished
                output_queue.put({"type":"success", "job":"transform"})
            except Exception as err:
                output_queue.put({"type":"error", "job":"transform", "message": str(err)})

        #Build the keras model
        elif job["command"] == "build_model":
            #Attempt to generate the model
            try:
                #Build the model
                model = build_model(project_path)

                #Inform the main thread that model generated properly
                output_queue.put({"type":"success", "job":"build_model"})

            except Exception as err:
                output_queue.put({"type":"error", "job":"build_model", "message": str(err)})

        #Train the keras model
        elif job["command"] == "train":
            #Attempt to train the model
            try:
                #Run training
                results = train(project_path, model, output_queue)

                #Save the model's most recent weights
                model.save_weights(path.join(project_path, "models", "latest.h5"))

                #Inform the main thread that the model trained properly
                output_queue.put({"type":"success", "job":"train", "message": results})

            except Exception as err:
                output_queue.put({"type":"error", "job":"train", "message": str(err)})

        elif job["command"] == "shutdown":
            break
