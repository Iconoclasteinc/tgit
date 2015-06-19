# -*- coding: utf-8 -*-
from datetime import datetime

from dateutil import tz

from .embedded_containers import load_metadata, save_metadata
from tgit import __app_name__, __version__
from tgit.track import Track


def load_track(filename):
    return Track(filename, load_metadata(filename))


def save_track(track, at_time=None):
    track.tagger = __app_name__
    track.tagger_version = __version__
    track.tagging_time = (at_time or datetime.now(tz.tzlocal())).strftime('%Y-%m-%d %H:%M:%S %z')
    save_metadata(track.filename, _all_metadata(track))


def _all_metadata(track):
    album_metadata = track.album.metadata.copy()
    if track.album.compilation:
        del album_metadata['lead_performer']
    track_metadata = track.metadata.copy()
    track_metadata.update(album_metadata)
    return track_metadata
