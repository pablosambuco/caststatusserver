# coding: utf-8
"""prueba."""
# pylint: disable=redefined-builtin
import time
from pprint import pprint as print
from caststatusserver import CastStatusServer

cast = CastStatusServer()
time.sleep(1)
cast.init()
time.sleep(1)
print(cast.update_list())

for cast_name in cast.casts:
    print(cast_name)
    time.sleep(1)

    status = cast.casts[cast_name].media_controller.status

    print(status.title)
    print(status.series_title)
    print(status.season)
    print(status.episode)
    print(status.artist)
    print(status.album_name)
    print(status.album_artist)
    print(status.track)
    print(status.duration)
    print(status.subtitle_tracks)
    print(status.current_subtitle_tracks)
    print(status.last_updated)
    print(status.player_state)
    print(status.current_time)
    print(status.content_id)
    print(status.content_type)
    print(status.supported_media_commands)
    print(status.stream_type)
