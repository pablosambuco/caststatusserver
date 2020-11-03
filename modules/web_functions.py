#!/usr/bin/python3
# -*- coding: utf-8 -*-
from bottle import run, get
import modules.db_functions as db

play="/images/play.png"
base="/images/base.png"
pause="/images/pause.png"

def html_from_mongo():
    events=db.read()

    html = "<!DOCTYPE html>"
    html += "<html>"
    html += "<body>"
    for dict in events:
        html += "<br/>"
        html += dict['clave']['listener'] + "<br/>"
        html += dict['clave']['cast'] + "<br/>"
        if('estado' in dict):
            html += dict['estado'] + "<br/>"
        if('volumen' in dict):
            html += dict['volumen'] + "<br/>"
        if('mute' in dict):
            html += dict['mute'] + "<br/>"
        if('titulo' in dict):
            html += dict['titulo'] + "<br/>"
        if('subtitulo' in dict):
            html += dict['subtitulo'] + "<br/>"
        if('serie' in dict):
            html += dict['serie'] + "<br/>"
        if('temporada' in dict):
            html += dict['temporada'] + "<br/>"       
        if('episodio' in dict):
            html += dict['episodio'] + "<br/>"       
        if('artista' in dict):
            html += dict['artista'] + "<br/>"       
        if('album_name' in dict):
            html += dict['album'] + "<br/>"       
        if('pista' in dict):
            html += dict['pista'] + "<br/>"       
        if('texto' in dict):
            html += dict['texto'] + "<br/>"       
        if('icono' in dict):
            html += dict['icono'] + "<br/>"       
        if('imagen' in dict):
            html += dict['imagen'] + "<br/>"             
    html += "</body>"
    html += "</html>"

    return html
   
@get('/')
def home():
    return html_from_mongo()

run(host='0.0.0.0', port=8083, debug=True)   
