# -*- coding: utf-8 -*-

from datetime import timedelta
from flexmock import flexmock


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

    return flexmock(**dict(defaults.items() + tags.items()))
