#!/usr/bin/python3
# -*- coding: utf-8 -*-
from bottle import Bottle, run, template, get, static_file, post, request, abort
import modules.custom_functions as f
import os, sys, time, logging
from logging.handlers import RotatingFileHandler
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketHandler, WebSocketError
from pathlib import Path

f.create_listeners()

Path("logs").mkdir(parents=True, exist_ok=True)
logger=logging.getLogger()
handler=RotatingFileHandler('logs/web.log', maxBytes=1048576, backupCount=5)
formatter=logging.Formatter('%(levelname)s %(asctime)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

dirname = os.path.dirname(sys.argv[0])

app = Bottle()
@app.route(r'/static/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root=dirname+'/static/css')
    
@app.route(r'/static/<filename:re:.*\.js>')
def send_js(filename):
    return static_file(filename, root=dirname+'/static/js')

@app.route(r'/images/<filename:re:.*\.png>')
def send_png(filename):
    return static_file(filename, root=dirname+'/static/images')      

@app.route('/')
def index():
    data = f.estados
    return template('index',data = data)

@app.post('/api')
def api():
    f.atender(request.body.getvalue().decode('utf-8'))
    return request.body

@app.route('/estado')
def estado():
    response={}
    for key in ['cast','estado','imagen','titulo','volumen','mute','uuid',]:
        response[key]=request.query.get(key,default="")
    return response

@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = wsock.receive()
            if(message=="init"):
                logger.info(message + " recibido. Enviando listado de dispositivos.")
                wsock.send(str(f.init()))    
            elif(message=="update"):
                logger.info(message + " recibido. Enviando estado de dispositivos.")
                wsock.send(str(f.get_status()))
            else:
                logger.warning(message + " recibido. No hay servicio asociado.")
        except WebSocketError:
            break

server = WSGIServer(("0.0.0.0", 8083), app, handler_class=WebSocketHandler)
server.serve_forever()

# run(app, host='0.0.0.0', port = 8083)
