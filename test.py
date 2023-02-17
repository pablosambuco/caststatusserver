# coding: utf-8
"""prueba."""
# pylint: disable=redefined-builtin
import time
import caststatusserver

cast = caststatusserver.instance
cast.init()
print(cast.casts)

for cast_name in cast.casts:
    print(cast_name)
    time.sleep(1)
    status = cast.casts[cast_name].media_controller.status
    print("  current_time:" + str(status.current_time))
    print("  content_id:" + str(status.content_id))
    print("  content_type:" + str(status.content_type))
    print("  duration:" + str(status.duration))
    print("  stream_type:" + str(status.stream_type))
    print("  idle_reason:" + str(status.idle_reason))
    print("  media_session_id:" + str(status.media_session_id))
    print("  playback_rate:" + str(status.playback_rate))
    print("  player_state:" + str(status.player_state))
    print("  supported_media_commands:" + str(status.supported_media_commands))
    print("  volume_level:" + str(status.volume_level))
    print("  volume_muted:" + str(status.volume_muted))
    print("  media_custom_data:" + str(status.media_custom_data))
    print("  media_metadata:" + str(status.media_metadata))
    print("  subtitle_tracks:" + str(status.subtitle_tracks))
    print("  current_subtitle_tracks:" + str(status.current_subtitle_tracks))
    print("  last_updated:" + str(status.last_updated))
    print("  adjusted_current_time:" + str(status.adjusted_current_time))
    print("  metadata_type:" + str(status.metadata_type))
    print("  player_is_playing:" + str(status.player_is_playing))
    print("  player_is_paused:" + str(status.player_is_paused))
    print("  player_is_idle:" + str(status.player_is_idle))
    print("  media_is_generic:" + str(status.media_is_generic))
    print("  media_is_tvshow:" + str(status.media_is_tvshow))
    print("  media_is_movie:" + str(status.media_is_movie))
    print("  media_is_musictrack:" + str(status.media_is_musictrack))
    print("  media_is_photo:" + str(status.media_is_photo))
    print("  stream_type_is_buffered:" + str(status.stream_type_is_buffered))
    print("  stream_type_is_live:" + str(status.stream_type_is_live))
    print("  title:" + str(status.title))
    print("  series_title:" + str(status.series_title))
    print("  season:" + str(status.season))
    print("  episode:" + str(status.episode))
    print("  artist:" + str(status.artist))
    print("  album_name:" + str(status.album_name))
    print("  album_artist:" + str(status.album_artist))
    print("  track:" + str(status.track))
    print("  images:" + str(status.images))
    print("  supports_pause:" + str(status.supports_pause))
    print("  supports_seek:" + str(status.supports_seek))
    print("  supports_stream_volume:" + str(status.supports_stream_volume))
    print("  supports_stream_mute:" + str(status.supports_stream_mute))
    print("  supports_skip_forward:" + str(status.supports_skip_forward))
    print("  supports_skip_backward:" + str(status.supports_skip_backward))
    print("  supports_queue_next:" + str(status.supports_queue_next))
    print("  supports_queue_prev:" + str(status.supports_queue_prev))
