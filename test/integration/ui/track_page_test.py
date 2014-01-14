# -*- coding: utf-8 -*-

from datetime import timedelta

from hamcrest import equal_to

from test.integration.ui.view_test import ViewTest
from test.cute.finders import WidgetIdentity
from test.cute.probes import AssertionProbe
from test.drivers.track_page_driver import TrackPageDriver
from test.util import builders as build

from tgit.ui.track_page import TrackPage


class TrackPageTest(ViewTest):
    def setUp(self):
        super(TrackPageTest, self).setUp()
        self.album = build.album()
        self.track = build.track(bitrate=192000,
                                 duration=timedelta(minutes=4, seconds=35).total_seconds())
        self.album.addTrack(self.track)
        self.widget = TrackPage(self.album, self.track)
        self.show(self.widget)
        self.driver = self.createDriverFor(self.widget)

    def createDriverFor(self, widget):
        return TrackPageDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysTrackMetadata(self):
        self.track.trackTitle = 'Song'
        self.driver.showsTrackTitle('Song')
        self.track.versionInfo = 'Remix'
        self.driver.showsVersionInfo('Remix')
        self.driver.showsBitrate('192 kbps')
        self.driver.showsTrackNumber('1')
        self.driver.showsTotalTracks('1')
        self.driver.showsDuration('04:35')
        self.track.featuredGuest = 'Featuring'
        self.driver.showsFeaturedGuest('Featuring')
        self.track.lyricist = 'Lyricist'
        self.driver.showsLyricist('Lyricist')
        self.track.composer = 'Composer'
        self.driver.showsComposer('Composer')
        self.track.publisher = 'Publisher'
        self.driver.showsPublisher('Publisher')
        self.track.isrc = 'Code'
        self.driver.showsIsrc('Code')
        self.driver.showsIswc('')
        self.track.tags = 'Tag1 Tag2 Tag3'
        self.driver.showsTags('Tag1 Tag2 Tag3')
        self.track.lyrics = 'Lyrics\n...\n...'
        self.driver.showsLyrics('Lyrics\n...\n...')
        self.track.language = 'eng'
        self.driver.showsLanguage('eng')
        self.driver.showsPreviewTime('00:00')

    def testUpdatesTotalNumberOfTracksWhenAlbumCompositionChanges(self):
        for i in xrange(11):
            self.album.addTrack(build.track())

        self.driver.showsTotalTracks('12')

    def testUpdatesTrackNumberWhenTrackPositionInAlbumChanges(self):
        for i in xrange(11):
            self.album.insertTrack(build.track(), 0)

        self.driver.showsTrackNumber('12')

    def testIgnoresUpdatesToAlbumCompositionWhenTrackRemovedFromAlbum(self):
        for i in xrange(11):
            self.album.addTrack(build.track())

        for track in self.album.tracks:
            self.album.removeTrack(track)

        assert True

    def testIgnoresUpdatesToTrackStateWhenTrackRemovedFromAlbum(self):
        self.album.removeTrack(self.track)
        self.widget.trackStateChanged(self.track)
        assert True

    def testUpdatesTrackWhenEdited(self):
        self.driver.changeTrackTitle('Song')
        self.check(AssertionProbe(self.track.trackTitle, equal_to('Song'), 'track title'))

        self.driver.changeVersionInfo('Remix')
        self.check(AssertionProbe(self.track.versionInfo, equal_to('Remix'), 'version info'))

        self.driver.changeFeaturedGuest('Featuring')
        self.check(AssertionProbe(self.track.featuredGuest, equal_to('Featuring'),
                                  'featured guest'))

        self.driver.changeLyricist('Lyricist')
        self.check(AssertionProbe(self.track.lyricist, equal_to('Lyricist'), 'lyricist'))

        self.driver.changeComposer('Composer')
        self.check(AssertionProbe(self.track.composer, equal_to('Composer'),  'composer'))

        self.driver.changePublisher('Publisher')
        self.check(AssertionProbe(self.track.publisher, equal_to('Publisher'), 'publisher'))

        self.driver.changeIsrc('Code')
        self.check(AssertionProbe(self.track.isrc, equal_to('Code'), 'isrc'))

        self.driver.changeTags('Tag1 Tag2 Tag3')
        self.check(AssertionProbe(self.track.tags, equal_to('Tag1 Tag2 Tag3'), 'tags'))

        self.driver.addLyrics('Lyrics')
        self.driver.addLyrics('...')
        self.check(AssertionProbe(self.track.lyrics, equal_to('Lyrics\n...\n'), 'lyrics'))

        self.driver.changeLanguage('eng')
        self.check(AssertionProbe(self.track.language, equal_to('eng'), 'language'))