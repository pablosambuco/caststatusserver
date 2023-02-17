#!/usr/bin/python3
"""Web.py: servidor principal de CastStatus."""

# pylint: disable=line-too-long,fixme,E1101,no-name-in-module

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
from caststatusserver import instance as CASTSTATUS

Path("logs").mkdir(parents=True, exist_ok=True)
LOGGER = logging.getLogger()
HANDLER = RotatingFileHandler(
    "logs/web.log", maxBytes=1024**2, backupCount=5
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
    """Redireccion de static/*.css a static/css/*.css."""
    root = DIRNAME + "/static/css"
    return static_file(filename, root=root)


@APP.get(r"/static/<filename:re:.*\.js>")
def send_js(filename):
    """Redireccion de static/*.js a static/js/*.js."""
    root = DIRNAME + "/static/js"
    return static_file(filename, root=root)


@APP.get(r"/images/<filename>")
def send_image(filename):
    """Redireccion de images/*.* a static/images/*.*."""
    root = DIRNAME + "/static/images"
    return static_file(filename, root=root)


def index(filename):
    """Ruta /."""
    # TODO Separar 100% el webserver del CastStatusServer.
    root = DIRNAME + "/static/html"
    return static_file(filename, root=root)


@APP.route("/websocket")
def handle_websocket():
    """Ruta WS /websocket."""
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
    """Ruta /doc."""
    redirect("/doc/index.html")


@APP.route("/")
@APP.route("/doc/<filename:path>")
def handle_doc(filename="index.html"):
    """Ruta Doxygen docs."""
    root = DIRNAME + "/doc"
    return static_file(filename, root=root)


@APP.get("/")
@APP.get("/<filename>")
def login(filename="index.html", *, error=""):
    """Ruta raiz,  formulario de login."""
    return template("login", filename=filename, error=error)


@APP.post("/")
def do_login():
    """Post para el login."""
    username = request.forms.get("username")
    password = request.forms.get("password")
    filename = request.forms.get("fn")

    if check_login(username, password):
        return index(filename)
    return login(filename, error="Invalid username/password")


def check_login(username, password):
    """Valida el login contra user.pass si existe."""
    params = bytes(username + ":" + password, encoding="UTF-8")

    userpass = "Og=="  # default: blank user and pass
    if os.path.isfile(PASSFILE):
        with open(PASSFILE, "r", encoding="utf-8") as passfile:
            userpass = str(passfile.readline())  # solo leo la primera linea
    return params == b64decode(userpass)


def get_interface():
    """Obtiene la interfaz donde debe levantarse el servidor."""
    interface = 0
    if os.path.exists("interface.cfg"):
        with open("interface.cfg", encoding="utf-8") as ifacefile:
            interface = int(ifacefile.read())
    return interface


def get_port():
    """Obtiene el puerto donde debe levantarse el servidor."""
    port = 0
    if os.path.exists("port.cfg"):
        with open("port.cfg", encoding="utf-8") as portfile:
            port = int(portfile.read())
    return port


SERVER = WSGIServer(
    (get_interface(), get_port()),
    DebuggedApplication(APP),
    handler_class=WebSocketHandler,
)
SERVER.serve_forever()
