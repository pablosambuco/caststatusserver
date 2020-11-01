# -*- coding: utf-8 -*-
import pychromecast
import zeroconf
import time
import db_functions as db
from uuid import UUID

def write_status(listener,status):
#Despues ver como sacar los datos por separado de cada chromecast
#Ver como levantar en vivo a una pagina
#Agregar botones de control para cada chromecast, play, pausa, stop, volumen (slider)
    dict={}

    dict['listener']=listener.__class__.__name__
    dict['cast']=str(listener.cast.device.friendly_name)

    if(hasattr(status,'player_state')):
       dict['estado']=status.player_state
    if(hasattr(status,'volume_level')):
       dict['volumen']=status.volume_level
    if(hasattr(status,'volume_muted')):
       dict['mute']=status.volume_muted
    if(hasattr(status,'title')):
       dict['titulo']=status.title
    if(hasattr(status,'media_metadata')):
       if('subtitle' in status.media_metadata):
          dict['subtitulo']=status.media_metadata['subtitle']
    if(hasattr(status,'series_title')):
       dict['serie']=status.series_title
    if(hasattr(status,'season')):
       dict['temporada']=status.season
    if(hasattr(status,'episode')):
       dict['episodio']=status.episode
    if(hasattr(status,'artist')):
       dict['artista']=status.artist
    if(hasattr(status,'album_name')):
       dict['album']=status.album_name
    if(hasattr(status,'track')):
       dict['pista']=status.track
    if(hasattr(status,'status_text')):
       dict['texto']=status.status_text
    if(hasattr(status,'icon_url')):
       dict['icono']=status.icon_url
    if(hasattr(status,'images')):
       if(len(status.images)>=1):
          if(hasattr(status.images[0],'url')):
             dict['imagen']=status.images[0].url
    
    print(dict)
    result = db.col.delete_many({'listener': listener.__class__.__name__})
    db.col.insert_one(dict)

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
