# -*- coding: utf-8 -*-
import pychromecast
import zeroconf
import time
import datetime
import requests
from uuid import UUID

dispositivos = []
ips = []
uuids = []
chromecasts = []
estados = {}


def send_status(listener, status):
    cast = str(listener.cast.device.friendly_name)
    listener_aux = listener.__class__.__name__

    # si no existe la clave la creo como un diccionario vacio
    if(cast not in estados):
        estados[cast] = {}
        estados[cast]['uuid'] = str(listener.cast.device.uuid)
        estados[cast]['cast'] = cast

    if(listener_aux == "StatusMediaListener"):
        if(hasattr(status, 'volume_level') and status.volume_level):
            estados[cast]['volumen'] = '{:.2f}'.format(status.volume_level)
        if(hasattr(status, 'title') and status.title):
            estados[cast]['titulo'] = status.title
        if(hasattr(status, 'media_metadata') and status.media_metadata):
            if('subtitle' in status.media_metadata):
                estados[cast]['subtitulo'] = status.media_metadata['subtitle']
        if(hasattr(status, 'series_title') and status.series_title):
            estados[cast]['serie'] = status.series_title
        if(hasattr(status, 'season') and status.season):
            estados[cast]['temporada'] = status.season
        if(hasattr(status, 'episode') and status.episode):
            estados[cast]['episodio'] = status.episode
        if(hasattr(status, 'artist') and status.artist):
            estados[cast]['artista'] = status.artist
        if(hasattr(status, 'album_name') and status.album_name):
            estados[cast]['album'] = status.album_name
        if(hasattr(status, 'track') and status.track):
            estados[cast]['pista'] = status.track
        if(hasattr(status, 'images')):
            if(len(status.images) >= 1):
                if(hasattr(status.images[0], 'url')):
                    estados[cast]['imagen'] = status.images[0].url
        if(hasattr(status, 'player_state') and status.player_state):
            estados[cast]['estado'] = status.player_state

    if(listener_aux == "StatusListener"):
        if(hasattr(status, 'volume_level') and status.volume_level):
            estados[cast]['volumen'] = '{:.2f}'.format(status.volume_level)
        if(hasattr(status, 'volume_muted') and status.volume_muted):
            estados[cast]['mute'] = status.volume_muted
        if(hasattr(status, 'status_text') and status.status_text):
            estados[cast]['texto'] = status.status_text
        if(hasattr(status, 'icon_url') and status.icon_url):
            estados[cast]['icono'] = status.icon_url

    # Si al terminar el loop, no tengo algunos datos, los completo con otros
    for cast in estados.keys():
        if('imagen' not in estados[cast] and 'icono' in estados[cast]):
            estados[cast]['imagen'] = estados[cast]['icono']
        if('titulo' not in estados[cast] and 'texto' in estados[cast]):
            estados[cast]['titulo'] = estados[cast]['texto']
        if('artista' not in estados[cast] and 'subtitulo' in estados[cast]):
            estados[cast]['artista'] = estados[cast]['subtitulo']

    estados[cast]['timestamp'] = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S")

    # Si al terminar el loop, no tengo algunos datos, borro el registro
    borrar = []
    for cast in estados.keys():
        if('estado' in estados[cast] and estados[cast]['estado'] == "UNKNOWN" and 'texto' not in estados[cast]):
            borrar.append(cast)
    for i in borrar:
        del estados[i]

    r = requests.get('http://127.0.0.1:8083/estado', params=estados)
    print(r.url)


class StatusListener:
    def __init__(self, name, cast):
        self.name = name
        self.cast = cast

    def new_cast_status(self, status):
        send_status(self, status)


class StatusMediaListener:
    def __init__(self, name, cast):
        self.name = name
        self.cast = cast

    def new_media_status(self, status):
        send_status(self, status)


def create_listeners():
    listener = pychromecast.CastListener()
    zconf = zeroconf.Zeroconf()
    browser = pychromecast.discovery.start_discovery(listener, zconf)
    time.sleep(1)
    for uuid, service in listener.services.items():
        cast = pychromecast.get_chromecast_from_service(service, zconf)
        if(service[2] == "Chromecast"):
            if service[3] not in dispositivos:
                cast.wait()
                listenerCast = StatusListener(cast.name, cast)
                cast.register_status_listener(listenerCast)
                listenerMedia = StatusMediaListener(cast.name, cast)
                cast.media_controller.register_status_listener(listenerMedia)
                dispositivos.append(service[3])
                ips.append(service[4])
                uuids.append(uuid)
                chromecasts.append(cast)

    pychromecast.stop_discovery(browser)


def atender(params):
    parametros = params.split(',')
    uuid = parametros[0].split('=')[1]
    cast = parametros[1].split('=')[1]
    accion = parametros[2].split('=')[1]
    parametro = parametros[3].split('=')[1]
    print(uuid + "-" + cast + "-" + accion + "-" + parametro)
    return
