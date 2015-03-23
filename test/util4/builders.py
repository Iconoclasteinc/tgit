# -*- coding: utf-8 -*-

from tgit4.metadata import Metadata, Image
from tgit4.album import Album
from tgit4.track import Track


def image(mime='image/jpeg', data='...', type_=Image.OTHER, desc=''):
    return mime, data, type_, desc


def metadata(images=(), **meta):
    metadata = Metadata(**meta)

    for image in images:
        metadata.addImage(*image)

    return metadata


def track(filename='track.mp3', metadata=None, **meta):
    track = Track(filename, metadata)

    for tag, value in meta.items():
        setattr(track, tag, value)

    return track


def album(images=(), tracks=(), **meta):
    album = Album()

    for tag, value in meta.items():
        setattr(album, tag, value)

    for image in images:
        album.addImage(*image)

    for track in tracks:
        album.addTrack(track)

    return album