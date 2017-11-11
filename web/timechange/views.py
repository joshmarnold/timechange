from web import settings
from web import app
from flask import render_template, redirect, flash, url_for, request

from .test import *

@app.route('/test')
def test():
    print("HYT")
    print( hello() )
    return ''
