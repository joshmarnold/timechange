from web import settings
from web import app
from flask import render_template, redirect, flash, url_for, request
from . import *



@app.route('/projectInit', methods=['POST'])
def projectInit():
    new_project(app.config['PROJECT_PATH']);
    return ''
