# -*- coding: utf-8 -*-
import pychromecast
import zeroconf
import time
from uuid import UUID

def show_status(status):
#Todo esto deberia ir a una base de datos... sqlite? 
#Despues ver como sacar los datos por separado de cada chromecast
#Ver como levantar en vivo a una pagina
#Agregar botones de control para cada chromecast, play, pausa, stop, volumen (slider)
    print("-------------------------------------")
    if(hasattr(status,'player_state')):
       print("Estado: " + status.player_state)
    if(hasattr(status,'volume_level')):
       print("Volumen: " + "{0:.0%}".format(status.volume_level))
    if(hasattr(status,'volume_muted')):
       print("Mute: " + str(status.volume_muted))
    if(hasattr(status,'title')):
       print("Titulo: " + str(status.title))
    if(hasattr(status,'series_title')):
       print("Serie: " + str(status.series_title))
    if(hasattr(status,'season')):
       print("Temporada: " + str(status.season))
    if(hasattr(status,'episode')):
       print("Episodio: " + str(status.episode))
    if(hasattr(status,'artist')):
       print("Artista: " + str(status.artist))
    if(hasattr(status,'album_name')):
       print("Album: " + str(status.album_name))
    if(hasattr(status,'album_artist')):
       print("Artista: " + str(status.album_artist))
    if(hasattr(status,'track')):
       print("Pista: " + str(status.track))
    if(hasattr(status,'status_text')):
       print("Texto: " + str(status.status_text))
    if(hasattr(status,'icon_url')):
       print("Icono: " + str(status.icon_url))
    if(hasattr(status,'images')):
       if(len(status.images)>=1):
          if(hasattr(status.images[0],'url')):
             print("Imagen: " + str(status.images[0].url))



class StatusListener:
    def __init__(self, name, cast):
        self.name = name
        self.cast = cast

    def new_cast_status(self, status):
        show_status(status)

class StatusMediaListener:
    def __init__(self, name, cast):
        self.name = name
        self.cast = cast

    def new_media_status(self, status):
        show_status(status)

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
