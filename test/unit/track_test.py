# -*- coding: utf-8 -*-

import unittest
from hamcrest import assert_that, equal_to, match_equality as matching, has_entries, has_property
from flexmock import flexmock

from tgit.album import TITLE as ALBUM_TITLE
from tgit.track import Track, TrackListener, TITLE, VERSION_INFO, ISRC, FEATURED_GUEST
from test.util import builders


class TrackTest(unittest.TestCase):
    def testReadsAudioInformationFromAudioFile(self):
        audio = builders.audio(filename='file.mp3',
                              bitrate=192000,
                              duration=210)
        track = Track(audio)
        assert_that(track.filename, equal_to('file.mp3'), 'filename')
        assert_that(track.bitrate, equal_to(192000), 'bitrate')
        assert_that(track.duration, equal_to(210), 'duration')

    def testInitiallyLoadsMetadataFromAudioFile(self):
        audio = builders.audio(trackTitle='Title',
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
            TITLE: 'Title',
            VERSION_INFO: 'Remix',
            FEATURED_GUEST: 'Featuring',
            ISRC: 'Code',
            ALBUM_TITLE: 'Album'
        }

        audio = builders.audio()
        track = Track(audio)
        track.trackTitle = metadata[TITLE]
        track.versionInfo = metadata[VERSION_INFO]
        track.featuredGuest = metadata[FEATURED_GUEST]
        track.isrc = metadata[ISRC]
        track.metadata[ALBUM_TITLE] = metadata[ALBUM_TITLE]

        audio.should_receive('save').with_args(matching(has_entries(**metadata))).once()
        track.tag()

    def testAnnouncesStateChangesToListener(self):
        self.assertNotifiesListenerOnPropertyChange('trackTitle', 'Title')
        self.assertNotifiesListenerOnPropertyChange('versionInfo', 'Remix')
        self.assertNotifiesListenerOnPropertyChange('featuredGuest', 'Featuring')
        self.assertNotifiesListenerOnPropertyChange('isrc', 'Code')

    def assertNotifiesListenerOnPropertyChange(self, property, value):
        track = Track(builders.audio())
        listener = flexmock(TrackListener())
        track.addTrackListener(listener)
        listener.should_receive('trackStateChanged') \
            .with_args(matching(has_property(property, value))) \
            .once()

        setattr(track, property, value)
