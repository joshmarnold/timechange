from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/home')
def home():
    if request.method == 'GET':
        return render_template("home.html")

@app.route('/loadFiles')
def loadFiles():
    if request.method == 'GET':
        return render_template("loadFiles.html")

@app.route('/transfromData')
def transformData():
    if request.method == 'GET':
        return render_template("transformData.html")

@app.route('/FFTPreview')
def FFTPreview():
    if request.method == 'GET':
        return render_template("FFTPreview.html")

@app.route('/configure')
def configure():
    if request.method == 'GET':
        return render_template("configure.html")

@app.route('/results')
def results():
    if request.method == 'GET':
        return render_template("results.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run()
