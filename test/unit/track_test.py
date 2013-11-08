# -*- coding: utf-8 -*-

import unittest
from hamcrest import (assert_that, equal_to, match_equality as matching, has_property )
from flexmock import flexmock

from test.util import builders as build

import tgit.tags as tags
from tgit.track import Track, TrackListener


class TrackTest(unittest.TestCase):
    def testReadsMetadataFromAudioFile(self):
        metadata = build.metadata(bitrate=19200,
                                  duration=210,
                                  trackTitle='Title',
                                  versionInfo='Remix',
                                  featuredGuest='Featuring',
                                  lyricist='Lyricist',
                                  composer='Composer',
                                  publisher='Publisher',
                                  isrc='Code')

        track = Track(build.audio('file.mp3', **metadata))
        assert_that(track.filename, equal_to('file.mp3'), 'filename')
        for tag, value in metadata.items():
            assert_that(track, has_property(tag, value), 'track')

    def testSavesAllMetadataToAudioFileWhenTagged(self):
        metadata = build.metadata(
            releaseName='Album',
            bitrate=19200,
            duration=210,
            trackTitle='Title',
            versionInfo='Remix',
            featuredGuest='Featuring',
            lyricist='Lyricist',
            composer='Composer',
            publisher='Publisher',
            isrc='Code',
            images=[build.image('image/jpeg', 'front-cover.jpg', desc='Front Cover')])

        audio = build.audio()
        track = Track(audio)

        for tag, value in metadata.copy(*tags.TRACK_TAGS).items():
            setattr(track, tag, value)

        audio.should_receive('save').with_args(metadata).once()
        track.tag(metadata.copy(tags.RELEASE_NAME))

    def testAnnouncesStateChangesToListener(self):
        self.assertNotifiesListenerOnPropertyChange('trackTitle', 'Title')
        self.assertNotifiesListenerOnPropertyChange('versionInfo', 'Remix')
        self.assertNotifiesListenerOnPropertyChange('featuredGuest', 'Featuring')
        self.assertNotifiesListenerOnPropertyChange('isrc', 'Code')

    def assertNotifiesListenerOnPropertyChange(self, prop, value):
        track = Track(build.audio())
        track.addTrackListener(self.listenerExpectingNotification(prop, value))
        setattr(track, prop, value)

    def listenerExpectingNotification(self, prop, value):
        listener = flexmock(TrackListener())
        listener.should_receive('trackStateChanged') \
            .with_args(matching(has_property(prop, value))) \
            .once()
        return listener
