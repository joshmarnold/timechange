from web import app
from flask import render_template, redirect, flash, url_for

ALLOWED_EXTENSIONS = set(['csv', 'xls', 'xlsx'])
UPLOAD_FOLDER = '/files'

# files to upload
#uploaded_csvs = UploadSet('files2upload', csv)
#configure_uploads(app, uploaded_images)

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/loadFiles')
def loadFiles():
    return render_template("loadFiles.html")

@app.route('/transfromData')
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
    target = os.path.join(APP_ROOT, 'csv/')
    print(target)

    # if images folder does not exist
    if not os.path.isdir(target):
        os.mkdir(target)

    # grab all the files
    # the files are objects containing
    # information on each object
    # in this case, file can be used to access
    # this information
    for file in request.files.getlist("input_files"): #input_files from html form
        print(file)
        # returns the file name of object bring uploaded
        filename = file.filename
        #create target destination(join target path with file name being uploaded)
        destination = "/".join([target, filename])
        print(destination)
        # save the file in the destination
        file.save(destination)



    # # check if the post request has the file part
    # if 'file' not in request.files:
    #     flash('No file part')
    #     return redirect(request.url)
    # file = request.files['file']
    # # if user does not select file, browser also
    # # submit a empty part without filename
    # if file.filename == '':
    #     flash('No selected file')
    #     return redirect(request.url)
    # if file and allowed_file(file.filename):
    #     filename = secure_filename(file.filename)
    #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #     return redirect(url_for('uploaded_file',
    #                             filename=filename))
    # return "uploaded successfully"
