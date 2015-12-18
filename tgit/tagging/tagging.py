# -*- coding: utf-8 -*-
from datetime import datetime, timezone

from tgit import __app_name__, __version__
from tgit.track import Track
from . import embedded_containers as containers


def load_track(filename):
    metadata = containers.load_metadata(filename)
    metadata = _unroll_isni_map(metadata)

    return Track(filename, metadata)


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

    _create_isni_map(track_metadata)

    return track_metadata


def _create_isni_map(track_metadata):
    if "lead_performer" in track_metadata:
        _unroll_identity_tuple("lead_performer", track_metadata)
    if "lyricist" in track_metadata:
        _unroll_identity_tuple("lyricist", track_metadata)


def _unroll_isni_map(metadata):
    if "lead_performer" in metadata:
        metadata = _transform_identity_to_tuple("lead_performer", metadata)
    if "lyricist" in metadata:
        metadata = _transform_identity_to_tuple("lyricist", metadata)
    return metadata


def _unroll_identity_tuple(field, metadata):
    identity = metadata[field]
    if not identity:
        return

    name = identity[0]
    metadata[field] = name


def _transform_identity_to_tuple(field, metadata):
    metadata[field] = (metadata[field],)

    return metadata
