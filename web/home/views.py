import sys
import os
import json
import shutil
import os.path as path
from web import settings
from web import app
from flask import render_template, redirect, flash, url_for, request, jsonify
from werkzeug import secure_filename


APP_ROOT = path.dirname(path.abspath(__file__))
ALLOWED_EXTENSIONS = set(['csv', 'xls', 'xlsx'])
PROJECT_PATH = path.join(APP_ROOT, '../default/')
app.config['PROJECT_PATH'] = PROJECT_PATH


# files to upload
#uploaded_csvs = UploadSet('files2upload', csv)
#configure_uploads(app, uploaded_images)

@app.route('/')
@app.route('/home')
def home():
    # Initialize function from __init__.py
    return render_template("home.html")

@app.route('/loadFiles')
def loadFiles():
    file_names = []
    return render_template("loadFiles.html", file_names=file_names)

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    file_names = []
    target = path.join(PROJECT_PATH, "csv/")

    #input_files from html form and save locally
    for file in request.files.getlist("file"):
        # if an empty form, return
        if file.filename == '':
            return render_template('loadFiles.html', file_names=file_names, flag='fail', message="Uh oh, you forgot to add files")
        file_names.append(secure_filename(file.filename))
        filename = secure_filename(file.filename)
        file.save(os.path.join(target, filename))
        file.close()

    return render_template('loadFiles.html', file_names=file_names, flag='success', message="Success")


@app.route('/getjson', methods=['POST'])
def getjson():
    print("in getjson")
    # path to files
    target = path.join(PROJECT_PATH, "csv/")

    event_data = request.get_json(cache=True)
    for x in range(0,5):
        return event_data['hello']

    # converts the JSON object into Python recognizable data
    #req_data = request.get_json()
    #print(req_data.is_json())

    #fileName_label = req_data['file_name']
    #print(fileName_label)
    # print(fileName_label)

    # for row in req_data:
    #     print(row['file_name'])
    #     add_training_file(row["label"],PROJECT_PATH, path.join(target, row['file_name']))

    # return "success!"
    # return (''), 204


@app.route('/alerts', methods=['POST'])
def alerts():

    print("HERE IN")


    return 'helllllo'
