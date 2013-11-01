# -*- coding: utf-8 -*-

from flexmock import flexmock

from tgit.metadata import Metadata, Image
from tgit.album import Album
from tgit.track import Track


def image(mime='image/jpeg', data='...', type_=Image.FRONT_COVER, desc=''):
    return mime, data, type_, desc


def metadata(bitrate=96000, duration=200, **meta):
    metadata = Metadata(bitrate=bitrate, duration=duration, **meta)
    if 'images' in meta:
        for image in meta['images']:
            metadata.addImage(*image)
        del metadata['images']
    return metadata


def audio(filename='track.mp3', **meta):
    return flexmock(filename=filename,
                    metadata=metadata(**meta),
                    save=lambda metadata: 'saved!')


def track(filename='track.mp3', **meta):
    return Track(audio(filename, **meta))


def album(**meta):
    tracks = []
    if 'tracks' in meta:
        for track in meta['tracks']:
            tracks.append(track)
        del meta['tracks']

    album = Album(metadata(**meta))
    for track in tracks:
        album.addTrack(track)
    return album