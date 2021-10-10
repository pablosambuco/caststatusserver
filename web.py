#!/usr/bin/python3
"""Web.py: servidor principal de CastStatus"""

# pylint: disable=line-too-long,fixme,E1101

import os
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from base64 import b64decode
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from bottle import Bottle, redirect, static_file, request, abort, template
from werkzeug.debug import DebuggedApplication
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

DIRNAME = os.path.dirname(os.path.realpath(__file__))
APP = Bottle()

PASSFILE = os.path.join(DIRNAME, "user.pass")


@APP.get(r"/static/<filename:re:.*\.css>")
def send_css(filename):
    """Redireccion de static/*.css a static/css/*.css

    Args:
        filename (string): Ruta del css a redirigir

    Returns:
        string Ruta del css redirigido
    """
    root = DIRNAME + "/static/css"
    return static_file(filename, root=root)


@APP.get(r"/static/<filename:re:.*\.js>")
def send_js(filename):
    """Redireccion de static/*.js a static/js/*.js

    Args:
        filename (string): Ruta del js a redirigir

    Returns:
        string Ruta del js redirigido
    """
    root = DIRNAME + "/static/js"
    return static_file(filename, root=root)


@APP.get(r"/images/<filename>")
def send_image(filename):
    """Redireccion de images/*.* a static/images/*.*

    Args:
        filename (string): Ruta de la imagen a redirigir

    Returns:
        string Ruta de la imagen redirigida
    """
    root = DIRNAME + "/static/images"
    return static_file(filename, root=root)


def index(filename):
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

@APP.route("/doc")
def handle_doc_root():
    """Ruta /doc

    Ruta para la documentación generada con doxygen

    """
    redirect("/doc/index.html")


@APP.route("/")
@APP.route("/doc/<filename:path>")
def handle_doc(filename="index.html"):
    """Ruta Doxygen docs
    Ruta utilizada para la documentacion
    """
    root = DIRNAME + "/doc"
    return static_file(filename, root=root)


@APP.get("/")
@APP.get("/<filename>")
def login(filename="index.html", *, error=""):
    """Ruta raiz,  formulario de login"""
    return template("login", filename=filename, error=error)


@APP.post("/")
def do_login():
    """Post para el login"""
    username = request.forms.get("username")
    password = request.forms.get("password")
    filename = request.forms.get("fn")

    if check_login(username, password):
        return index(filename)
    return login(filename, error="Invalid username/password")


def check_login(username, password):
    """Valida el login contra user.pass si existe"""
    params = bytes(username + ":" + password, encoding="UTF-8")

    userpass = "dXNlcjpwYXNz"  # default: user:pass
    if os.path.isfile(PASSFILE):
        with open(PASSFILE, "r", encoding="utf-8") as passfile:
            userpass = str(passfile.readline())  # solo leo la primera linea
    return params == b64decode(userpass)


SERVER = WSGIServer(
    ("192.168.1.40", 8083),
    DebuggedApplication(APP),
    handler_class=WebSocketHandler,
)
SERVER.serve_forever()
# APP.run(host='192.168.1.40', port=8083)
