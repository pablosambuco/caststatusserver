#!/usr/bin/python3
# -*- coding: utf-8 -*-
from bottle import Bottle, run, template, get, static_file
import modules.db_functions as db
import modules.web_functions as web
import modules.custom_functions as f
import os, sys

play="/images/play.png"
base="/images/base.png"
pause="/images/pause.png"
dirname = os.path.dirname(sys.argv[0])

app = Bottle()
@app.route('/static/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root=dirname+'/static/css')
    
@app.route('/static/<filename:re:.*\.js>')
def send_css(filename):
    return static_file(filename, root=dirname+'/static/js')

@app.route('/images/<filename:re:.*\.png>')
def send_css(filename):
    return static_file(filename, root=dirname+'/static/images')      

@app.route('/')
def index():
    data = f.parse(db.read())
    return template('index',data = data)

run(app, host='0.0.0.0', port = 8083)
