import sys
import os
import json
import shutil
import os.path as path
from web import settings
from web import app
from flask import render_template, redirect, flash, url_for, request, jsonify
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['csv', 'xls', 'xlsx'])
PROJECT_PATH = path.join(path.dirname(path.abspath(__file__)), '../default/')
app.config['PROJECT_PATH'] = PROJECT_PATH

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_default_dir():
    # create default dir
    os.mkdir(PROJECT_PATH)
    # under default create csv dir
    os.mkdir(os.path.join(PROJECT_PATH, 'csv/'))
    # under csv create labels dir
    os.mkdir(os.path.join(PROJECT_PATH, 'csv/labels/'))
    # under default create images dir
    os.mkdir(os.path.join(PROJECT_PATH, 'images/'))
    # under default create models dir
    os.mkdir(os.path.join(PROJECT_PATH, 'models/'))

def remove_default_dir():
    shutil.rmtree(PROJECT_PATH)

def remove_and_create_labels_dir():
    shutil.rmtree(os.path.join(PROJECT_PATH, 'csv/labels/'))
    os.mkdir(os.path.join(PROJECT_PATH, 'csv/labels/'))

def create_directory(post_data):
    # for each labels
    for index in range(len(post_data)):
        #if label-name folder exists in label folder
        if os.path.isdir(os.path.join(PROJECT_PATH, 'csv/labels/' + post_data[index]['label'])):
            # move file from csv folder to label-name folder
            shutil.move(os.path.join(PROJECT_PATH, 'csv/' + post_data[index]['file_name']), os.path.join(PROJECT_PATH, 'csv/labels/' + post_data[index]['label']))
        else:
            # create label-name folder in label folder
            os.mkdir(os.path.join(PROJECT_PATH, 'csv/labels/' + post_data[index]['label']))
            # move file in csv folder to new label-name folder
            shutil.move(os.path.join(PROJECT_PATH, 'csv/' + post_data[index]['file_name']), os.path.join(PROJECT_PATH, 'csv/labels/' + post_data[index]['label']))

@app.route('/')
@app.route('/home')
def home():
    # Initialize function from __init__.py
    return render_template("home.html")

@app.route('/initProject', methods=['POST'])
def initProject():
    # if default dir exists
    # delete and create
    if os.path.isdir(PROJECT_PATH):
        remove_default_dir();
        create_default_dir();
    else:
        create_default_dir();
    return (''), 204

@app.route('/loadFiles')
def loadFiles():
    file_names = []
    return render_template("loadFiles.html", file_names=file_names, slideUp=True)

@app.route('/transformData')
def transformData():
    return render_template("transformData.html")

@app.route('/FFTPreview')
def FFTPreview():
    return render_template("FFTPreview.html")

@app.route('/configure')
def configure():
    return render_template("configure.html")

@app.route('/results')
def results():
    return render_template("results.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/upload', methods=['POST'])
def upload():
    file_names = []
    target = path.join(PROJECT_PATH, "csv/")

    #input_files from html form and save locally
    for file in request.files.getlist("file"):
        # if an empty form, return
        if file.filename == '':
            return render_template('loadFiles.html', file_names=file_names, flag='fail', message="Uh oh, you forgot to add files", slideUp=False)
        file_names.append(secure_filename(file.filename))
        filename = secure_filename(file.filename)
        file.save(os.path.join(target, filename))
        file.close()

    return render_template('loadFiles.html', file_names=file_names, flag='success', message="Success", slideUp=False)

@app.route('/getjson', methods=['POST'])
def getjson():
    print("in getjson")
    # path to files
    target = path.join(PROJECT_PATH, "csv/")

    post_data = request.get_json()

    print( post_data[4]['file_name'] )

    create_directory(post_data)

    # for row in req_data:
    #     print(row['file_name'])
    #     add_training_file(row["label"],PROJECT_PATH, path.join(target, row['file_name']))

    # return "success!"
    return (''), 204


@app.route('/alerts', methods=['POST'])
def alerts():

    print("HERE IN")


    return 'helllllo'
