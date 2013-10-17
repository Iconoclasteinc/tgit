# -*- coding: utf-8 -*-

from datetime import timedelta
from flexmock import flexmock

from tgit.metadata import Metadata, Image


class Double(object):
    def __init__(self, **attrs):
        for name, value in attrs.iteritems():
            setattr(self, name, value)

    def __repr__(self):
        return "(%s)" % ', '.join(
            ["%s=%s" % (name, str(getattr(self, name))) for name in self.__dict__])


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


# todo should go away
def track(**tags):
    defaults = dict(filename='track.mp3',
                    releaseName=None,
                    frontCoverPicture=(None, None),
                    leadPerformer=None,
                    guestPerformers=None,
                    labelName=None,
                    recordingTime=None,
                    releaseTime=None,
                    originalReleaseTime=None,
                    upc=None,
                    trackTitle=None,
                    versionInfo=None,
                    featuredGuest=None,
                    isrc=None,
                    bitrate=96000,
                    duration=timedelta(minutes=3, seconds=30).total_seconds())
    metadata = dict(defaults.items() + tags.items())
    return Double(**metadata)