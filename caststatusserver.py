"""Modulo conteniendo las clases necesarias para el manejo de chromecasts."""
# pylint: disable=line-too-long,fixme,consider-using-dict-items,unused-argument

import time
import datetime

# import logging
import json
import zeroconf
from geventwebsocket import WebSocketError, WebSocketServer
from pychromecast.controllers.media import MediaStatus
from pychromecast import (
    Chromecast,
    get_chromecast_from_cast_info,
    CastListener,
    discovery,
    stop_discovery,
)


# TODO Convertir el GenericListener en abstracto con ABC
class GenericListener:
    """Clase listener generica."""

    def __init__(self, server, cast: Chromecast, listener_type):
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
        """Metodo para enviar cambios de medios.
        Args:
            status (Response): Estado que se envia al diccionario de estados
        """
        self.server.update_status(self, status)

    def new_connection_status(self, status):
        """Metodo para enviar cambios de medios.
        Args:
            status (Response): Estado que se envia al diccionario de estados
        """
        self.server.update_status(self, status)


# TODO Tratar de crear un módulo para dejar de usar singleton
class CastStatusServerMeta(type):
    """Clase con funcionalidades de busqueda y control de Chromecasts en una red local.

    Esta clase contiene una instancia de tipo CastStatusSingleton.

    Todos los metodos son derivados a esa instancia unica que atiende todos
    los pedidos.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Prueba."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class CastStatusServer(metaclass=CastStatusServerMeta):
    """Singleton (?)."""

    def __init__(self):
        self.casts = {}
        self.status = {}
        self.wsocks: list(WebSocketServer) = []

        listener = CastListener()
        zconf = zeroconf.Zeroconf()
        browser = discovery.start_discovery(listener, zconf)
        time.sleep(1)
        for _, service in listener.services.items():
            cast = get_chromecast_from_cast_info(service, zconf)
            if service[2] == "Chromecast" and service[3] not in self.casts:
                cast.wait()
                slist = GenericListener(self, cast, "status")
                cast.register_status_listener(slist)
                mlist = GenericListener(self, cast, "media")
                cast.media_controller.register_status_listener(mlist)
                clist = GenericListener(self, cast, "connection")
                cast.register_connection_listener(clist)
                self.casts[service[3]] = cast

        stop_discovery(browser)

    def __str__(self):
        return str(self.casts)

    def init(self):
        """Devuelve el listado de nombres de chromecasts.

        Returns:
            list listado de nombres de chromecasts
        """
        return self.casts

    def update_list(self) -> dict:
        """Devuelve el listado de nombres de chromecasts.

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

    def update_status(
        self, listener: GenericListener, status: MediaStatus
    ) -> None:
        """Actualiza el diccionario de estados.

        Args:
            listener (Listener): objeto listener que llama a este metodo
            status (MediaStatus): respuesta del cast con el cambio de estado
        """
        cast = str(listener.cast.device.friendly_name)
        # si no existe la clave la creo como un diccionario vacio
        if cast not in self.status.keys():
            self.status[cast] = {}
            self.status[cast]["prev_volume"] = None

        attr_lookup = get_attribs(listener.listener_type, status)
        for attr in attr_lookup:
            if attr_lookup[attr]:
                self.status[cast][map_key(attr)] = attr_lookup[attr]

        self.set_substitutes(cast)

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status[cast]["timestamp"] = now

        self.send()

    def atender(self, wsock: WebSocketServer) -> None:
        """Funcion para atender los mensajes del WebSocket.

        Args:
            wsock (WebSocket): objeto donde se recibiran los mensajes

        Raises:
            exc: Si ocurre una excepcion de WebSocket se envia
        """
        try:
            message = wsock.receive()
            if message == "init":
                wsocks: list(WebSocketServer) = []
                wsocks.append(wsock)
                for auxsock in self.wsocks:
                    if not auxsock.closed:
                        wsocks.append(auxsock)
                self.wsocks = list(set(wsocks))
                self.send()
                return

            if message == "update":
                self.update(wsock)
                return

            if message:
                comando = message.split(",")
                metodo = getattr(self, comando[0], None)
                cast_name = comando[1]
                parametros = None
                if len(comando) > 2:
                    parametros = comando[2]

                if metodo:
                    metodo(cast_name, parametros)

                # TODO: agregar comandos para activar o descativar los
                # subtitulos

        except WebSocketError as exc:
            raise exc

    def update(self, wsock: WebSocketServer) -> None:
        """Actualiza el listado de chromecasts.

        Args:
            wsock (WebSocket): objeto donde se recibiran los mensajes
        """
        for cast_name in self.status:
            controller = self.casts[cast_name].media_controller

            duration = controller.status.duration
            current_time = controller.status.adjusted_current_time

            self.status[cast_name]["position"] = 0
            if duration and current_time:
                self.status[cast_name]["position"] = current_time / duration

        self.send(wsock)

    def back(self, cast_name: str, value=None) -> None:
        """Back.

        Args:
            cast (Chromecast): Cast en el que se aplica el back
        """
        try:
            self.casts[cast_name].media_controller.queue_prev()
            self.casts[cast_name].media_controller.rewind()
        except AttributeError:
            pass

    def play(self, cast_name: str, value=None) -> None:
        """Play.

        Args:
            cast (Chromecast): Cast en el que se aplica el play
        """
        try:
            self.casts[cast_name].media_controller.play()
        except (AttributeError, KeyError):
            pass

    def pause(self, cast_name: str, value=None) -> None:
        """Pause.

        Args:
            cast (Chromecast): Cast en el que se aplica el pause
        """
        try:
            self.casts[cast_name].media_controller.pause()
        except (AttributeError, KeyError):
            pass

    def forward(self, cast_name: str, value=None) -> None:
        """Forward.

        Args:
            cast (Chromecast): Cast en el que se aplica el forward
        """
        try:
            self.casts[cast_name].media_controller.skip()
        except (AttributeError, KeyError):
            pass

    def forward10(self, cast_name: str, value=None) -> None:
        """Forward 10.
        Args:
            cast (Chromecast): Cast en el que se aplica el forward
        """
        try:
            ctime = self.casts[cast_name].media_controller.status.current_time
            self.casts[cast_name].media_controller.seek(ctime + 10)
        except (AttributeError, KeyError):
            pass

    def back10(self, cast_name: str, value=None) -> None:
        """Back 10.
        Args:
            cast (Chromecast): Cast en el que se aplica el back
        """
        try:
            ctime = self.casts[cast_name].media_controller.status.current_time
            self.casts[cast_name].media_controller.seek(ctime - 10)
        except (AttributeError, KeyError):
            pass

    def volume(self, cast_name: str, value: float) -> None:
        """Cambio de Volumen.

        Args:
            cast (Chromecast): Cast en el que se aplica el volumen
            value (int): Valor de 0 a 100 para aplicar
        """
        try:
            self.casts[cast_name].set_volume(float(value) / 100)
            self.status[cast_name]["prev_volume"] = value
        except (AttributeError, KeyError):
            pass

    def mute(self, cast_name: str, value=None) -> None:
        """Mute.

        Args:
            cast (Chromecast): Cast en el que se aplica el volumen
        """
        try:
            self.casts[cast_name].set_volume(0)
        except (AttributeError, KeyError):
            pass

    def unmute(self, cast_name: str, value=None) -> None:
        """Unmute.

        Args:
            cast (Chromecast): Cast en el que se aplica el volumen
        """
        try:
            value = self.status[cast_name]["prev_volume"]
            # si ya estaba reproduciendo y no tengo idea del volumen, uso 50%
            if not value:
                value = 50
            self.casts[cast_name].set_volume(float(value) / 100)
        except (AttributeError, KeyError):
            pass

    def position(self, cast_name: str, value: float) -> None:
        """Cambio de Posicion.

        Args:
            cast (Chromecast): Cast en el que se aplica la posicion
            value (int): Valor de 0 a 100 para aplicar
        """
        try:
            duration = self.casts[cast_name].media_controller.status.duration
            new_position = (float(value) / 100) * duration
            self.casts[cast_name].media_controller.seek(new_position)
Es deLO¢²¢
        except (AttributeError, KeyError):
            pass

    def set_state(self) -> None:
        """Metodo para establecer el estado o borrar la tarjeta en el front"""
        borrar = []
        for cast in self.status:
            try:
                chromecast = self.casts[cast]
            except KeyError:
                chromecast = None
            #  Si el reproductor esta en un estado desconocido, lo marco
            if (
                not chromecast
                or chromecast.media_controller.status.player_state == "UNKNOWN"
                or chromecast.app_id is None
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

    def set_substitutes(self, cast_name: str) -> None:
        """Metodo de reemplazo de atributos
            Podria ser inutil si mejora la asignacion original

        Args:
            cast (String): friendly_name del Cast
        """
        lookup = {
            "image": ["icon"],
            "title": ["text"],
            "artist": ["episode", "subtitle"],
            "subtitle": ["series"],
        }
        # Completo datos con sus reemplazos y borro claves si es necesario
        for orig in lookup:
            subs = lookup[orig]
            for sub in subs:
                if sub in self.status[cast_name]:
                    if (
                        orig not in self.status[cast_name]
                        or not self.status[cast_name][orig]
                    ):
                        self.status[cast_name][orig] = self.status[cast_name][
                            sub
                        ]
                    elif (
                        self.status[cast_name][orig]
                        != self.status[cast_name][sub]
                    ):
                        del self.status[cast_name][sub]

    def send(self, wsock: WebSocketServer = None) -> None:
        """Metodo para enviar el estado actual a todos los websockets"""
        self.set_state()
        message = json.dumps(self.update_list())
        if wsock and not wsock.closed:
            wsock.send(message)
            return
        for iwsock in self.wsocks:
            if not iwsock.closed:
                iwsock.send(message)


def map_key(key) -> str:
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
        "app_id": "app_id",
        "position": "position",
    }
    return lookup[key]


def get_attribs(listener_type: str, status: MediaStatus) -> dict:
    """Parse de los atributos del estado

    Args:
        listener_type (string): tipo de listener que detecta el cambio
        status (MediaStatus): Objeto con el estado actual
    """
    # TODO Tener en cuenta el metadataType
    # https://developers.google.com/cast/docs/reference/messages#MediaStatus
    #  con este dato se puede decidir què atributos buscar y simplificar el
    #  diccionario de estados
    #  0: GenericMediaMetadata: title, subtitle, images
    #  1: MovieMediaMetadata: title, subtitle, images, studio
    #  2: TvShowMediaMetadata: seriesTitle, subtitle, season, episode, images
    #  3: MusicTrackMediaMetadata: title, albumName, artist, images
    #  4: PhotoMediaMetadata: title, artist, location
    #

    # TODO Determinar que comandos estan permitidos (atributo
    # supportedMediaCommands) para enviar al frontend que botones deben estar
    # disponibles
    # MediaStatus: playerState, supportedMediaCommands, volume
    #
    try:
        status_image = status.images[0].url
    except (AttributeError, KeyError, IndexError):
        status_image = None

    try:
        app_id = status.app_id
    except (AttributeError, KeyError):
        app_id = None

    lookup = {}
    if listener_type == "media":
        lookup = {
            "volume_level": f"{status.volume_level:.2f}",
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
            "position": status.current_time / status.duration,
        }
    elif listener_type == "status":
        lookup = {
            "volume_level": f"{status.volume_level:.2f}",
            "volume_muted": status.volume_muted,
            "status_text": status.status_text,
            "icon_url": status.icon_url,
            "app_id": app_id,
        }
    elif listener_type == "connection":
        lookup = {
            "player_state": status.status,
        }

    for key in lookup:
        if lookup[key] and str(lookup[key]).isspace():
            lookup[key] = None

    return lookup
