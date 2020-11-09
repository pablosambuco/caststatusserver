# -*- coding: utf-8 -*-
import pychromecast
import zeroconf
import time
import datetime
import modules.db_functions as db
from uuid import UUID


def write_status(listener, status):
    # Despues ver como sacar los datos por separado de cada chromecast
    # Ver como levantar en vivo a una pagina
    # Agregar botones de control para cada chromecast, play, pausa, stop, volumen (slider)
    dict = {}
    clave = {}

    clave['listener'] = listener.__class__.__name__
    clave['cast'] = str(listener.cast.device.friendly_name)

    dict['clave'] = clave
    dict['uuid'] = str(listener.cast.device.uuid)

    if(hasattr(status, 'player_state') and status.player_state):
        dict['estado'] = status.player_state
    if(hasattr(status, 'volume_level') and status.volume_level):
        dict['volumen'] = '{:.2f}'.format(status.volume_level)
    if(hasattr(status, 'volume_muted') and status.volume_muted):
        dict['mute'] = status.volume_muted
    if(hasattr(status, 'title') and status.title):
        dict['titulo'] = status.title
    if(hasattr(status, 'media_metadata') and status.media_metadata):
        if('subtitle' in status.media_metadata):
            dict['subtitulo'] = status.media_metadata['subtitle']
    if(hasattr(status, 'series_title') and status.series_title):
        dict['serie'] = status.series_title
    if(hasattr(status, 'season') and status.season):
        dict['temporada'] = status.season
    if(hasattr(status, 'episode') and status.episode):
        dict['episodio'] = status.episode
    if(hasattr(status, 'artist') and status.artist):
        dict['artista'] = status.artist
    if(hasattr(status, 'album_name') and status.album_name):
        dict['album'] = status.album_name
    if(hasattr(status, 'track') and status.track):
        dict['pista'] = status.track
    if(hasattr(status, 'status_text') and status.status_text):
        dict['texto'] = status.status_text
    if(hasattr(status, 'icon_url') and status.icon_url):
        dict['icono'] = status.icon_url
    if(hasattr(status, 'images')):
        if(len(status.images) >= 1):
            if(hasattr(status.images[0], 'url')):
                dict['imagen'] = status.images[0].url

    dict['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if(hasattr(status, 'player_state') and status.player_state == "UNKNOWN"):
        db.delete(dict, 'clave')
    else:
        db.write(dict, 'clave')


class StatusListener:
    def __init__(self, name, cast):
        self.name = name
        self.cast = cast

    def new_cast_status(self, status):
        write_status(self, status)


class StatusMediaListener:
    def __init__(self, name, cast):
        self.name = name
        self.cast = cast

    def new_media_status(self, status):
        write_status(self, status)


dispositivos = []
ips = []
uuids = []
chromecasts = []


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


def parse(data):
    resultados = {}

    for fila in list(data):
        cast = fila['clave']['cast']
        listener = fila['clave']['listener']

        # si no existe la clave la creo como un diccionario vacio
        if(cast not in resultados):
            resultados[cast] = {}

        if(listener == "StatusMediaListener"):
            if('uuid' in fila):
                resultados[cast]['uuid'] = fila['uuid']
            if('volumen' in fila):
                resultados[cast]['volumen'] = fila['volumen']
            if('titulo' in fila):
                resultados[cast]['titulo'] = fila['titulo']
            if('subtitulo' in fila):
                resultados[cast]['subtitulo'] = fila['subtitulo']
            if('serie' in fila):
                resultados[cast]['serie'] = fila['serie']
            if('temporada' in fila):
                resultados[cast]['temporada'] = fila['temporada']
            if('episodio' in fila):
                resultados[cast]['episodio'] = fila['episodio']
            if('artista' in fila):
                resultados[cast]['artista'] = fila['artista']
            if('album' in fila):
                resultados[cast]['album'] = fila['album']
            if('pista' in fila):
                resultados[cast]['pista'] = fila['pista']
            if('imagen' in fila):
                resultados[cast]['imagen'] = fila['imagen']
            if('estado' in fila):
                resultados[cast]['estado'] = fila['estado']

        if(listener == "StatusListener"):
            if('uuid' in fila):
                resultados[cast]['uuid'] = fila['uuid']
            if('volumen' in fila):
                resultados[cast]['volumen'] = fila['volumen']
            if('mute' in fila):
                resultados[cast]['mute'] = fila['mute']
            if('texto' in fila):
                resultados[cast]['texto'] = fila['texto']
            if('icono' in fila):
                resultados[cast]['icono'] = fila['icono']

    # Si al terminar el loop, no tengo algunos datos, los completo con otros
    for cast in resultados.keys():
        if('imagen' not in resultados[cast] and 'icono' in resultados[cast]):
            resultados[cast]['imagen'] = resultados[cast]['icono']
        if('titulo' not in resultados[cast] and 'texto' in resultados[cast]):
            resultados[cast]['titulo'] = resultados[cast]['texto']
        if('artista' not in resultados[cast] and 'subtitulo' in resultados[cast]):
            resultados[cast]['artista'] = resultados[cast]['subtitulo']

    # Si al terminar el loop, no tengo algunos datos, borro el registro
    borrar = []
    for cast in resultados.keys():
        if('estado' not in resultados[cast] and 'texto' not in resultados[cast]):
            borrar.append(cast)
    for i in borrar:
        del resultados[i]

    return resultados


def atender(params):
    parametros = params.split(',')
    uuid=parametros[0].split('=')[1]
    cast=parametros[1].split('=')[1]
    accion=parametros[2].split('=')[1]
    parametro=parametros[3].split('=')[1]
    print(uuid + "-" + cast + "-" + accion + "-" + parametro)
    return
