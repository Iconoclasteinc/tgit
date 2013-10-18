# -*- coding: utf-8 -*-

from flexmock import flexmock

from tgit.metadata import Metadata, Image
from tgit.album import Album
from tgit.track import Track


def picture(mime='image/jpeg', data='...', type_=Image.FRONT_COVER, desc=''):
    return mime, data, type_, desc


def metadata(**meta):
    metadata = Metadata(**meta)
    if 'pictures' in meta:
        for picture in meta['pictures']:
            metadata.addImage(*picture)
        del metadata['pictures']
    return metadata


def audio(filename='track.mp3', bitrate=9600, duration=180, **meta):
    return flexmock(filename=filename, bitrate=bitrate, duration=duration,
                    metadata=lambda: metadata(**meta),
                    save=lambda metadata: 'saved!')


def track(filename='track.mp3', bitrate=9600, duration=180, **meta):
    return Track(audio(filename, bitrate, duration, **meta))


def album(**meta):
    return Album(metadata(**meta))
