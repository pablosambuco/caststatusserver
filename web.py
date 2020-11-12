#!/usr/bin/python3
# -*- coding: utf-8 -*-
from bottle import Bottle, run, template, get, static_file, post, request, abort
import modules.custom_functions as f
import os, sys, time
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketHandler, WebSocketError

f.create_listeners()

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
    print(response)
    return response

@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = wsock.receive()
            print(message)
            wsock.send("tu vieja")
        except WebSocketError:
            break

server = WSGIServer(("0.0.0.0", 8083), app, handler_class=WebSocketHandler)
server.serve_forever()

# run(app, host='0.0.0.0', port = 8083)
