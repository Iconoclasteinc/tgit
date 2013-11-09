# -*- coding: utf-8 -*-

from flexmock import flexmock

from tgit.metadata import Metadata, Image
from tgit.album import Album
from tgit.track import Track


def image(mime='image/jpeg', data='...', type_=Image.OTHER, desc=''):
    return mime, data, type_, desc


def metadata(bitrate=96000, duration=200, **meta):
    metadata = Metadata(bitrate=bitrate, duration=duration, **meta)
    if 'images' in meta:
        for image in meta['images']:
            metadata.addImage(*image)
        del metadata['images']
    return metadata


def track(filename='track.mp3', **meta):
    # todo album tags go in metadata
    # track tags are set via attributes
    return Track(filename, metadata(**meta))


def album(**meta):
    album = Album()
    if 'tracks' in meta:
        for track in meta['tracks']:
            album.addTrack(track)
        del meta['tracks']
    if 'images' in meta:
        for image in meta['images']:
            album.addImage(*image)
        del meta['images']

    for tag, value in meta.items():
        setattr(album, tag, value)

    return album