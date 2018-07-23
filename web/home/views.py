# web import
import sys
import os
import shutil
import os.path as path
from web import settings
from web import app
from flask import render_template, redirect, flash, url_for, request
from werkzeug import secure_filename


APP_ROOT = path.dirname(path.abspath(__file__))
ALLOWED_EXTENSIONS = set(['csv', 'xls', 'xlsx'])
UPLOAD_FOLDER = path.join(APP_ROOT, 'csv/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/home')
def home():
    # Initialize function from __init__.py
    return render_template("home.html")

@app.route('/loadFiles')
def loadFiles():
    file_names = []
    flag = ""
    return render_template("loadFiles.html", file_names=file_names, flag=flag)

@app.route('/transformData')
def transformData():
    print("heroer")
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
    target = path.join(APP_ROOT, UPLOAD_FOLDER)

    # delete current csv directory
    if os.path.isdir(target):
        shutil.rmtree(target)

    # mk a new directory
    os.mkdir(target)

    #input_files from html form and save locally
    for file in request.files.getlist("file"):
        # if an empty form, return
        if file.filename == '':
            return render_template('loadFiles.html', file_names=file_names, message="Uh oh, you forgot to add files", flag="fail")
        file_names.append(secure_filename(file.filename))
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file.close()

    return render_template('loadFiles.html', file_names=file_names, message="Success!", flag="success")


@app.route('/grabjson', methods=['POST'])
def grabjson():


    # converts the JSON object into Python recognizable data
    req_data = request.get_json()

    fileName_label = req_data['file_name']['label'][0]

    for row in fileName_label:
        print(row)


    return ''


@app.route('/alerts', methods=['POST'])
def alerts():

    return ''
