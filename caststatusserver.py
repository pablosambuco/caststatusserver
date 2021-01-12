# -*- coding: utf-8 -*-
"""Modulo conteniendo las clases necesarias para el manejo de chromecasts
"""

# pylint: disable=line-too-long,fixme

import time
import datetime
import logging
import unittest
import json
import zeroconf
from geventwebsocket import WebSocketError
import pychromecast



class CastStatusServer:
    """Clase con funcionalidades de busqueda y control de
    Chromecasts en una red local

    Esta clase contiene una instancia de tipo CastStatusSingleton.

    Todos los metodos son derivados a esa instancia unica que atiende todos
    los pedidos.
    """

    instance = None

    def __new__(cls):
        if not CastStatusServer.instance:
            CastStatusServer.instance = CastStatusServer.CastStatusSingleton()
        return CastStatusServer.instance

    def __getattr__(self, name):
        """Singleton getattr"""
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        """Singleton setattr"""
        return setattr(self.instance, name, value)

    class CastStatusSingleton:
        """Singleton (?)"""

        def __init__(self):
            self.casts = {}
            self.status = {}
            self.wsocks = []

            listener = pychromecast.CastListener()
            zconf = zeroconf.Zeroconf()
            browser = pychromecast.discovery.start_discovery(listener, zconf)
            time.sleep(1)
            for _, service in listener.services.items():
                cast = pychromecast.get_chromecast_from_service(service, zconf)
                if service[2] == "Chromecast":
                    if service[3] not in self.casts:
                        cast.wait()
                        slist = GenericListener(self, cast, "status")
                        cast.register_status_listener(slist)
                        mlist = GenericListener(self, cast, "media")
                        cast.media_controller.register_status_listener(mlist)
                        clist = GenericListener(self, cast, "connection")
                        cast.register_connection_listener(clist)
                        self.casts[service[3]] = cast

            pychromecast.stop_discovery(browser)

        def __str__(self):
            return str(self.casts)

        def init(self):
            """Devuelve el listado de nombres de chromecasts

            Returns:
                list listado de nombres de chromecasts
            """
            return self.casts

        def update(self):
            """Devuelve el listado de nombres de chromecasts

            Returns:
                list listado de nombres de chromecasts
            """
            lista = []
            for cast in self.status:
                aux = {}
                aux["cast"] = cast
                aux["contenido"] = self.status[cast]
                lista.append(aux)
            respuesta = {}
            respuesta["chromecasts"] = lista

            return respuesta

        def update_status(self, listener, status):
            """Actualiza el diccionario de estados

            Args:
                listener (Listener): objeto listener que llama a este metodo
                status (MediaStatus): respuesta del cast con el cambio de estado
            """
            cast = str(listener.cast.device.friendly_name)
            # si no existe la clave la creo como un diccionario vacio
            if cast not in self.status:
                self.status[cast] = {}

            attr_lookup = get_attribs(listener.listener_type, status)
            for attr in attr_lookup:
                if hasattr(status, attr) and attr_lookup[attr] is not None:
                    self.status[cast][map_key(attr)] = attr_lookup[attr]

            self.set_substitutes(cast)


            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.status[cast]["timestamp"] = now

            self.send()

        def atender(self, wsock):
            """Funcion para atender los mensajes del WebSocket

            Args:
                wsock (WebSocket): objeto donde se recibiran los mensajes

            Raises:
                exc: Si ocurre una excepcion de WebSocket se envia
            """
            logger = logging.getLogger()
            try:
                message = wsock.receive()
                if message == "init":
                    wsocks = []
                    wsocks.append(wsock)
                    for auxsock in self.wsocks:
                        if not auxsock.closed:
                            wsocks.append(auxsock)
                    self.wsocks = list(set(wsocks))
                    self.send()

                elif message:
                    log = message + " recibido"
                    comando = message.split(",")
                    if len(comando) == 2 and comando[0] == "play":
                        self.play(cast=comando[1])
                    elif comando[0] == "pause":
                        self.pause(cast=comando[1])
                    elif comando[0] == "back":
                        self.back(cast=comando[1])
                    elif comando[0] == "forward":
                        self.forward(cast=comando[1])
                    elif comando[0] == "volume":
                        self.volume(cast=comando[1], value=comando[2])
                    else:
                        logger.info("%s", log)
            except WebSocketError as exc:
                raise exc

        def back(self, cast):
            """Back

            Args:
                cast (Chromecast): Cast en el que se aplica el back
            """
            try:
                self.casts[cast].media_controller.queue_prev()
                self.casts[cast].media_controller.rewind()
            except AttributeError:
                pass

        def play(self, cast):
            """Play

            Args:
                cast (Chromecast): Cast en el que se aplica el play
            """
            try:
                self.casts[cast].media_controller.play()
            except AttributeError:
                pass
            except KeyError:
                pass

        def pause(self, cast):
            """Pause

            Args:
                cast (Chromecast): Cast en el que se aplica el pause
            """
            try:
                self.casts[cast].media_controller.pause()
            except AttributeError:
                pass
            except KeyError:
                pass

        def forward(self, cast):
            """Forward

            Args:
                cast (Chromecast): Cast en el que se aplica el forward
            """
            try:
                self.casts[cast].media_controller.seek(
                    self.status[cast].get("duration", 9999)
                )
            except AttributeError:
                pass
            except KeyError:
                pass

        def volume(self, cast, value):
            """Cambio de Volumen

            Args:
                cast (Chromecast): Cast en el que se aplica el volumen
                value (int): Valor de 0 a 100 para aplicar
            """
            try:
                self.casts[cast].set_volume(float(value) / 100)
            except AttributeError:
                pass
            except KeyError:
                pass

        def set_state(self):
            """Metodo para establecer el estado o borrar la tarjeta en el front
            """
            borrar = []
            for cast in self.status:
                #  Si el reproductor esta en un estado desconocido, lo marco
                if (
                        self.casts[cast].media_controller.status.player_state == "UNKNOWN"
                        or self.casts[cast].app_id is None
                ):
                    self.status[cast]["state"] = "REMOVE"
                    borrar.append(cast)
                else:
                    lookup = {
                        "IDLE": "PAUSED",  # podria ser tambien REMOVE
                        "PLAYING": "PLAYING",
                        "BUFFERING": "PLAYING",
                        "PAUSED": "PAUSED",
                    }

                    self.status[cast]["state"] = lookup[self.status[cast]["state"]]
            for cast in borrar:
                self.status.pop(cast, None)

        def set_substitutes(self, cast):
            """Metodo de reemplazo de atributos
                Podria ser inutil si mejora la asignacion original

            Args:
                cast (String): friendly_name del Cast
            """
            lookup = {
                "image": "icon",
                "title": "text",
                "subtitle": "series",
                "artist": "subtitle",
            }
            # Completo datos con sus reemplazos y borro claves si es necesario
            for orig in lookup:
                subs = lookup[orig]
                if subs in self.status[cast]:
                    if orig not in self.status[cast]:
                        self.status[cast][orig] = self.status[cast][subs]
                    elif self.status[cast][orig] != self.status[cast][subs]:
                        del self.status[cast][subs]

        def send(self):
            """Metodo para enviar el estado actual a todos los websockets"""
            self.set_state()
            message = json.dumps(self.update())
            for wsock in self.wsocks:
                if not wsock.closed:
                    wsock.send(message)


class GenericListener:
    """Clase listener generica"""

    def __init__(self, server, cast, listener_type):
        self.server = server
        self.cast = cast
        self.listener_type = listener_type

    def new_cast_status(self, status):
        """Metodo para enviar cambios de estado

        Args:
            status (Response): Estado que se envia al diccionario de estados
        """
        self.server.update_status(self, status)

    def new_media_status(self, status):
        """Metodo para enviar cambios de medios
        Args:
            status (Response): Estado que se envia al diccionario de estados
        """
        self.server.update_status(self, status)

    def new_connection_status(self, status):
        """Metodo para enviar cambios de medios
        Args:
            status (Response): Estado que se envia al diccionario de estados
        """
        self.server.update_status(self, status)


def map_key(key):
    """Funcion para mapear las claves"""
    lookup = {
        "volume_level": "volume",
        "title": "title",
        "subtitle": "subtitle",
        "series_title": "series",
        "season": "season",
        "episode": "episode",
        "artist": "artist",
        "album_name": "album",
        "track": "track",
        "images": "image",
        "player_state": "state",
        "volume_muted": "mute",
        "status_text": "text",
        "icon_url": "icon",
        "duration": "duration",
    }
    return lookup[key]


def get_attribs(listener_type, status):
    """Parse de los atributos del estado

    Args:
        listener_type (string): tipo de listener que detecta el cambio
        status (MediaStatus): Objeto con el estado actual
    """
    # TODO Tener en cuenta el metadataType (https://developers.google.com/cast/docs/reference/messages#MediaStatus)
    #  con este dato se puede decidir què atributos buscar y simplificar el diccionario de estados
    #  0: GenericMediaMetadata: title, subtitle, images
    #  1: MovieMediaMetadata: title, subtitle, images, studio
    #  2: TvShowMediaMetadata: seriesTitle, subtitle, season, episode, images
    #  3: MusicTrackMediaMetadata: title, albumName, artist, images
    #  4: PhotoMediaMetadata: title, artist, location
    #

    # TODO Determinar que comandos estan permitidos (atributo supportedMediaCommands) para enviar al frontend que botones deben estar disponibles
    #  MediaStatus: playerState, supportedMediaCommands, volume
    #
    try:
        status_image = status.images[0].url
    except AttributeError:
        status_image = None
    except KeyError:
        status_image = None

    lookup = {}
    if listener_type == "media":
        lookup = {
            "volume_level": "{:.2f}".format(status.volume_level),
            "title": status.title,
            "subtitle": status.media_metadata.get("subtitle"),
            "series_title": status.series_title,
            "season": status.season,
            "episode": status.episode,
            "artist": status.artist,
            "album_name": status.album_name,
            "player_state": status.player_state,
            "track": status.track,
            "images": status_image,
            "duration": status.duration,
        }
    elif listener_type == "status":
        lookup = {
            "volume_level": "{:.2f}".format(status.volume_level),
            "volume_muted": status.volume_muted,
            "status_text": status.status_text,
            "icon_url": status.icon_url,
            "app_id": status.app_id,
        }
    elif listener_type == "connection":
        lookup = {
            "player_state": status.status,
        }

    return lookup

if __name__ == '__main__':
    unittest.main()
