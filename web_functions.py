# -*- coding: utf-8 -*-
from bottle import run, get

def html_from_mongo():
    html = "<!DOCTYPE html>"
    html += "<html>"
    html += "<body>"
    html += "It' alive!!!"
    html += "</body>"
    html += "</html>"

    return html
   
@get('/')
def home():
    return html_from_mongo()

run(host='0.0.0.0', port=8083, debug=True)   
