# -*- coding: utf-8 -*-

import unittest
from hamcrest import assert_that, equal_to, match_equality as matching, has_entries, has_property
from flexmock import flexmock

from test.util import builders as build

from tgit.metadata import Metadata
import tgit.tags as tags
from tgit.track import Track, TrackListener


class TrackTest(unittest.TestCase):
    def testReadsAudioInformationFromAudioFile(self):
        audio = build.audio(filename='file.mp3',
                            bitrate=192000,
                            duration=210)
        track = Track(audio)
        assert_that(track.filename, equal_to('file.mp3'), 'filename')
        assert_that(track.bitrate, equal_to(192000), 'bitrate')
        assert_that(track.duration, equal_to(210), 'duration')

    def testInitiallyLoadsMetadataFromAudioFile(self):
        audio = build.audio(trackTitle='Title',
                            versionInfo='Remix',
                            featuredGuest='Featuring',
                            isrc='Code')
        track = Track(audio)
        assert_that(track.trackTitle, equal_to('Title'), 'title')
        assert_that(track.versionInfo, equal_to('Remix'), 'info')
        assert_that(track.featuredGuest, equal_to('Featuring'), 'featured guest')
        assert_that(track.isrc, equal_to('Code'), 'isrc')

    def testSavesMetadataToAudioFileWhenTagged(self):
        metadata = {
            tags.RELEASE_NAME: 'Album',
            tags.TRACK_TITLE: 'Title',
            tags.VERSION_INFO: 'Remix',
            tags.FEATURED_GUEST: 'Featuring',
            tags.ISRC: 'Code',
        }

        audio = build.audio()
        audio.should_receive('save').with_args(matching(has_entries(**metadata))).once()

        track = Track(audio)
        track.trackTitle = metadata[tags.TRACK_TITLE]
        track.versionInfo = metadata[tags.VERSION_INFO]
        track.featuredGuest = metadata[tags.FEATURED_GUEST]
        track.isrc = metadata[tags.ISRC]
        albumMetadata = Metadata(**metadata).select(tags.RELEASE_NAME)
        track.tag(albumMetadata)

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
