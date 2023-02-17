"""Modulo conteniendo las clases necesarias para el manejo de chromecasts."""

# pylint: disable=line-too-long,fixme,consider-using-dict-items,unused-argument
import contextlib
import datetime
import json
from abc import ABC
from geventwebsocket import WebSocketError, WebSocketServer
from pychromecast.controllers.media import MediaStatus
from pychromecast import (
    Chromecast,
    get_chromecasts,
)


# TODO Convertir el GenericListener en abstracto con ABC
class AbstractListener(ABC):
    """Clase listener abstracta."""

    def __init__(self, server, cast: Chromecast, listener_type):
        """Constructor de la clase."""
        self.server = server
        self.cast = cast
        self.listener_type = listener_type

    def new_cast_status(self, status):
        """
        Metodo para enviar cambios de estado.

        Args:
            status (Response): Estado que se envia al diccionario de estados
        """
        self.server.update_status(self, status)

    def new_media_status(self, status):
        """
        Metodo para enviar cambios de medios.

        Args:
            status (Response): Estado que se envia al diccionario de estados
        """
        self.server.update_status(self, status)

    def new_connection_status(self, status):
        """
        Metodo para enviar cambios de medios.

        Args:
            status (Response): Estado que se envia al diccionario de estados
        """
        self.server.update_status(self, status)


class MediaListener(AbstractListener):
    """Media"""

    def __init__(self, server, cast: Chromecast):
        super().__init__(server, cast, "media")


class StatusListener(AbstractListener):
    """Status"""

    def __init__(self, server, cast: Chromecast):
        super().__init__(server, cast, "status")


class ConnectionListener(AbstractListener):
    """Connection"""

    def __init__(self, server, cast: Chromecast):
        super().__init__(server, cast, "connection")


class CastStatusServer:
    """Server"""

    def __init__(self):
        """Constructor de la clase."""
        self.casts = {}
        self.status = {}
        self.wsocks: list(WebSocketServer) = []

        casts = get_chromecasts()[0]
        for cast in casts:
            cast.wait()
            slist = StatusListener(self, cast)
            cast.register_status_listener(slist)
            mlist = MediaListener(self, cast)
            cast.media_controller.register_status_listener(mlist)
            clist = ConnectionListener(self, cast)
            cast.register_connection_listener(clist)
            self.casts[cast.name] = cast

    def __str__(self):
        """Funcion para convertir en cadena."""
        return str(self.casts)

    def init(self):
        """
        Devuelve el listado de nombres de chromecasts.

        Returns:
            list listado de nombres de chromecasts
        """
        return self.casts

    def update_list(self) -> dict:
        """
        Devuelve el listado de nombres de chromecasts.

        Returns:
            list listado de nombres de chromecasts
        """
        lista = []
        for cast in self.status:
            aux = {"cast": cast, "contenido": self.status[cast]}
            lista.append(aux)
        return {"chromecasts": lista}

    def update_status(
        self, listener: AbstractListener, status: MediaStatus
    ) -> None:
        """
        Actualiza el diccionario de estados.

        Args:
            listener (Listener): objeto listener que llama a este metodo
            status (MediaStatus): respuesta del cast con el cambio de estado
        """
        cast = str(listener.cast.name)
        # si no existe la clave la creo como un diccionario vacio
        if cast not in self.status:
            self.status[cast] = {"prev_volume": None}
        attr_lookup = get_attribs(listener.listener_type, status)
        for attr in attr_lookup:
            if attr_lookup[attr]:
                self.status[cast][map_key(attr)] = attr_lookup[attr]

        self.set_substitutes(cast)

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status[cast]["timestamp"] = now

        self.send()

    def atender(self, wsock: WebSocketServer) -> None:
        """
        Funcion para atender los mensajes del WebSocket.

        Args:
            wsock (WebSocket): objeto donde se recibiran los mensajes

        Raises:
            exc: Si ocurre una excepcion de WebSocket se envia
        """
        try:
            message = wsock.receive()
            if message == "init":
                wsocks: list(WebSocketServer) = [wsock]
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
                parametros = comando[2] if len(comando) > 2 else None
                if metodo:
                    metodo(cast_name, parametros)

                    # TODO: agregar comandos para activar o descativar los
                    # subtitulos

        except WebSocketError as exc:
            raise exc

    def update(self, wsock: WebSocketServer) -> None:
        """
        Actualiza el listado de chromecasts.

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
        """
        Back.

        Args:
            cast (Chromecast): Cast en el que se aplica el back
        """
        with contextlib.suppress(AttributeError):
            self.casts[cast_name].media_controller.queue_prev()
            self.casts[cast_name].media_controller.rewind()

    def play(self, cast_name: str, value=None) -> None:
        """
        Play.

        Args:
            cast (Chromecast): Cast en el que se aplica el play
        """
        with contextlib.suppress(AttributeError, KeyError):
            self.casts[cast_name].media_controller.play()

    def pause(self, cast_name: str, value=None) -> None:
        """
        Pause.

        Args:
            cast (Chromecast): Cast en el que se aplica el pause
        """
        with contextlib.suppress(AttributeError, KeyError):
            self.casts[cast_name].media_controller.pause()

    def forward(self, cast_name: str, value=None) -> None:
        """
        Forward.

        Args:
            cast (Chromecast): Cast en el que se aplica el forward
        """
        with contextlib.suppress(AttributeError, KeyError):
            self.casts[cast_name].media_controller.skip()

    def forward10(self, cast_name: str, value=None) -> None:
        """
        Forward 10.

        Args:
            cast (Chromecast): Cast en el que se aplica el forward
        """
        with contextlib.suppress(AttributeError, KeyError):
            ctime = self.casts[cast_name].media_controller.status.current_time
            self.casts[cast_name].media_controller.seek(ctime + 10)

    def back10(self, cast_name: str, value=None) -> None:
        """
        Back 10.

        Args:
            cast (Chromecast): Cast en el que se aplica el back
        """
        with contextlib.suppress(AttributeError, KeyError):
            ctime = self.casts[cast_name].media_controller.status.current_time
            self.casts[cast_name].media_controller.seek(ctime - 10)

    def volume(self, cast_name: str, value: str) -> None:
        """
        Cambio de Volumen.

        Args:
            cast (Chromecast): Cast en el que se aplica el volumen
            value (int): Valor de 0 a 100 para aplicar
        """
        with contextlib.suppress(AttributeError, KeyError):
            self.casts[cast_name].set_volume(float(value) / 100)
            self.status[cast_name]["prev_volume"] = float(value)

    def mute(self, cast_name: str, value=None) -> None:
        """
        Mute.

        Args:
            cast (Chromecast): Cast en el que se aplica el volumen
        """
        with contextlib.suppress(AttributeError, KeyError):
            self.casts[cast_name].set_volume(0)

    def unmute(self, cast_name: str, value=None) -> None:
        """
        Unmute.

        Args:
            cast (Chromecast): Cast en el que se aplica el volumen
        """
        with contextlib.suppress(AttributeError, KeyError):
            value = self.status[cast_name]["prev_volume"] or 50
            self.casts[cast_name].set_volume(float(value) / 100)

    def position(self, cast_name: str, value: str) -> None:
        """
        Cambio de Posicion.

        Args:
            cast (Chromecast): Cast en el que se aplica la posicion
            value (int): Valor de 0 a 100 para aplicar
        """
        with contextlib.suppress(AttributeError, KeyError):
            duration = self.casts[cast_name].media_controller.status.duration
            new_position = float(value) / 100 * duration
            self.casts[cast_name].media_controller.seek(new_position)

    def set_state(self) -> None:
        """Metodo para establecer el estado o borrar la tarjeta en el front."""
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
        """
        Metodo de reemplazo de atributos.
        Podria ser inutil si mejora la asignacion original

        Args:
            cast (String): name del Cast
        """
        lookup = {
            "image": ["icon"],
            "title": ["text"],
            "artist": ["episode", "subtitle"],
            "subtitle": ["series"],
        }
        # Completo datos con sus reemplazos y borro claves si es necesario
        for orig, subs in lookup.items():
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
        """Metodo para enviar el estado actual a todos los websockets."""
        self.set_state()
        message = json.dumps(self.update_list())
        if wsock and not wsock.closed:
            wsock.send(message)
            return
        for iwsock in self.wsocks:
            if not iwsock.closed:
                iwsock.send(message)


def map_key(key) -> str:
    """Funcion para mapear las claves."""
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
    """
    Parse de los atributos del estado.

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
            "position": status.current_time / status.duration
            if status.duration
            else 0,
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

    for key, value in lookup.items():
        if value and str(value).isspace():
            lookup[key] = None

    return lookup


instance = CastStatusServer()
