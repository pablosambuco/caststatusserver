#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Web.py: servidor principal de CastStatus
"""

# pylint: disable=line-too-long,fixme

import os
import sys
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from bottle import Bottle
from bottle import static_file
from bottle import request
from bottle import abort
from caststatusserver import CastStatusServer

CASTSTATUS = CastStatusServer()

Path("logs").mkdir(parents=True, exist_ok=True)
LOGGER = logging.getLogger()
HANDLER = RotatingFileHandler(
    "logs/web.log", maxBytes=1024 * 1024, backupCount=5
)
FORMATTER = logging.Formatter("%(levelname)s %(asctime)s %(message)s")
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)
LOGGER.setLevel(logging.INFO)

DIRNAME = os.path.dirname(sys.argv[0])

APP = Bottle()


@APP.route(r"/static/<filename:re:.*\.css>")
def send_css(filename):
    """Redireccion de static/*.css a static/css/*.css

    Args:
        filename (string): Ruta del css a redirigir

    Returns:
        string Ruta del css redirigido
    """
    root = DIRNAME + "/static/css"
    return static_file(filename, root=root)


@APP.route(r"/static/<filename:re:.*\.js>")
def send_js(filename):
    """Redireccion de static/*.js a static/js/*.js

    Args:
        filename (string): Ruta del js a redirigir

    Returns:
        string Ruta del js redirigido
    """
    root = DIRNAME + "/static/js"
    return static_file(filename, root=root)


@APP.route(r"/images/<filename:re:.*\.png>")
def send_png(filename):
    """Redireccion de images/*.png a static/images/*.png

    Args:
        filename (string): Ruta del png a redirigir

    Returns:
        string Ruta del png redirigido
    """
    root = DIRNAME + "/static/images"
    return static_file(filename, root=root)


@APP.route("/")
@APP.route("/<filename>")
def index(filename="index.html"):
    """Ruta /

    Correspode a la pagina principal de la aplicacion

    Returns:
        HTML: contenido procesado a partir del template
    """
    # TODO Separar 100% el webserver del CastStatusServer. Ofrecer websocket desde el Cast.
    #  Esto implica sacar las variables del template de index, y crear una funcion en js para dibujar todo desde cero. ver a que nivel hay que insertar los objetos
    root = DIRNAME + "/static/html"
    return static_file(filename, root=root)


@APP.route("/websocket")
def handle_websocket():
    """Ruta WS /websocket

    Ruta utilizada para la comunicacion entre JavaScript (AJAX/JQuery) y Python

    """
    wsock = request.environ.get("wsgi.websocket")
    if not wsock:
        abort(400, "Expected WebSocket request.")

    while True:
        try:
            CASTSTATUS.atender(wsock)
        except WebSocketError:
            break


# @APP.route('/doc')
# def handle_doc():
#     """Ruta Doxygen docs

#     Ruta utilizada para la documentacion

#     """
#     return static_file('index.html', root=DIRNAME+'/html')


SERVER = WSGIServer(("0.0.0.0", 8083), APP, handler_class=WebSocketHandler)
SERVER.serve_forever()
