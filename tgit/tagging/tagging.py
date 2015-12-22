# -*- coding: utf-8 -*-
from datetime import datetime, timezone

from tgit import __app_name__, __version__
from tgit.track import Track
from . import embedded_containers as containers


def load_track(filename):
    return Track(filename, containers.load_metadata(filename))


def save_track(track, at_time=None):
    track.tagger = __app_name__
    track.tagger_version = __version__
    track.tagging_time = _in_utc(at_time).strftime("%Y-%m-%d %H:%M:%S %z")
    containers.save_metadata(track.filename, _all_metadata(track))


def _in_utc(at_time):
    return at_time and at_time.astimezone(timezone.utc) or datetime.now(timezone.utc)


def _all_metadata(track):
    album_metadata = track.album.metadata.copy()
    if track.album.compilation:
        del album_metadata["lead_performer"]
    track_metadata = track.metadata.copy()
    track_metadata.update(album_metadata)
    track_metadata["isnis"] = clean_isnis(track_metadata)

    return track_metadata


def clean_isnis(track_metadata):
    new_isni_map = {}
    isnis = track_metadata["isnis"] or {}
    lead_performer = track_metadata["lead_performer"]
    lyricist = track_metadata["lyricist"]
    if lead_performer in isnis:
        new_isni_map[lead_performer] = isnis[lead_performer]
    if lyricist in isnis:
        new_isni_map[lyricist] = isnis[lyricist]
    return new_isni_map
