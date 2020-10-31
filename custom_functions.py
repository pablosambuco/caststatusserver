# -*- coding: utf-8 -*-
import pychromecast
import zeroconf
import time
from uuid import UUID

def write_status(listener,status):
#Despues ver como sacar los datos por separado de cada chromecast
#Ver como levantar en vivo a una pagina
#Agregar botones de control para cada chromecast, play, pausa, stop, volumen (slider)
    cast=None
    estado=None
    volumen=None
    mute=None
    titulo=None
    subtitulo=None
    serie=None
    temporada=None
    episodio=None
    artista=None
    album=None
    pista=None
    texto=None
    icono=None
    imagen=None

    cast=str(listener.cast.device.friendly_name)

    if(hasattr(status,'player_state')):
       estado=status.player_state
    if(hasattr(status,'volume_level')):
       volumen=status.volume_level
    if(hasattr(status,'volume_muted')):
       mute=status.volume_muted
    if(hasattr(status,'title')):
       titulo=status.title
    if(hasattr(status,'media_metadata')):
       if('subtitle' in status.media_metadata):
          subtitulo=status.media_metadata['subtitle']
    if(hasattr(status,'series_title')):
       serie=status.series_title
    if(hasattr(status,'season')):
       temporada=status.season
    if(hasattr(status,'episode')):
       episodio=status.episode
    if(hasattr(status,'artist')):
       artista=status.artist
    if(hasattr(status,'album_name')):
       album=status.album_name
    if(hasattr(status,'track')):
       pista=status.track
    if(hasattr(status,'status_text')):
       texto=status.status_text
    if(hasattr(status,'icon_url')):
       icono=status.icon_url
    if(hasattr(status,'images')):
       if(len(status.images)>=1):
          if(hasattr(status.images[0],'url')):
             imagen=status.images[0].url
    
    print("tipo     : " + listener.__class__.__name__)
    print("cast     : " + str(cast      ))
    print("estado   : " + str(estado    ))
    print("volumen  : " + str(volumen   ))
    print("mute     : " + str(mute      ))
    print("titulo   : " + str(titulo    ))
    print("subtitulo: " + str(subtitulo ))
    print("serie    : " + str(serie     ))
    print("temporada: " + str(temporada ))
    print("episodio : " + str(episodio  ))
    print("artista  : " + str(artista   ))
    print("album    : " + str(album     ))
    print("pista    : " + str(pista     ))
    print("texto    : " + str(texto     ))
    print("icono    : " + str(icono     ))
    print("imagen   : " + str(imagen    ))


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

dispositivos=[]
ips=[]
uuids=[]
chromecasts=[]

def buscar():
    listener = pychromecast.CastListener()
    zconf = zeroconf.Zeroconf()
    browser = pychromecast.discovery.start_discovery(listener, zconf)
    time.sleep(1)
    for uuid, service in listener.services.items():
        cast = pychromecast.get_chromecast_from_service(service,zconf)
        if(service[2]=="Chromecast"):
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
