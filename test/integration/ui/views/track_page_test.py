# -*- coding: utf-8 -*-

from datetime import timedelta
from PyQt4.QtGui import QWidget
from hamcrest import has_properties

# noinspection PyUnresolvedReferences
import use_sip_api_v2

from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe
from test.drivers import TrackPageDriver
from test.integration.ui import ViewTest
from test.util import builders as build

from tgit.ui.views import TrackPage


class TrackPageTest(ViewTest):
    def setUp(self):
        super(TrackPageTest, self).setUp()
        self.album = build.album()
        self.view = TrackPage()
        self.widget = QWidget()
        self.view.render(self.widget)
        self.show(self.widget)
        self.driver = self.createDriverFor(self.widget)

    def createDriverFor(self, widget):
        return TrackPageDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysTrackMetadata(self):
        track = build.track(bitrate=192000,
                            duration=timedelta(minutes=4, seconds=35).total_seconds(),
                            trackTitle='Song',
                            versionInfo='Remix',
                            featuredGuest='Featuring',
                            lyricist='Lyricist',
                            composer='Composer',
                            publisher='Publisher',
                            isrc='Code',
                            tags='Tag1 Tag2 Tag3',
                            lyrics='Lyrics\n...\n...',
                            language='eng')
        album = build.album(tracks=[build.track(), build.track()])
        album.insertTrack(track, 0)

        self.view.refresh(album, track)

        self.driver.showsTrackTitle('Song')
        self.driver.showsVersionInfo('Remix')
        self.driver.showsBitrate('192 kbps')
        self.driver.showsDuration('04:35')
        self.driver.showsTrackNumber('1')
        self.driver.showsTotalTracks('3')
        self.driver.showsFeaturedGuest('Featuring')
        self.driver.showsLyricist('Lyricist')
        self.driver.showsComposer('Composer')
        self.driver.showsPublisher('Publisher')
        self.driver.showsIsrc('Code')
        self.driver.showsIswc('')
        self.driver.showsTags('Tag1 Tag2 Tag3')
        self.driver.showsLyrics('Lyrics\n...\n...')
        self.driver.showsLanguage('eng')
        self.driver.showsPreviewTime('00:00')

    def testSignalsWhenTrackMetadataEdited(self):
        changes = ValueMatcherProbe('track changed')

        class TrackChangedListener(object):
            def metadataEdited(self, state):
                changes.received(state)

        self.view.announceTo(TrackChangedListener())

        changes.expect(has_properties(trackTitle='Title'))
        self.driver.changeTrackTitle('Title')
        self.check(changes)

        changes.expect(has_properties(versionInfo='Remix'))
        self.driver.changeVersionInfo('Remix')
        self.check(changes)

        changes.expect(has_properties(featuredGuest='Featuring'))
        self.driver.changeFeaturedGuest('Featuring')
        self.check(changes)

        changes.expect(has_properties(lyricist='Lyricist'))
        self.driver.changeLyricist('Lyricist')
        self.check(changes)

        changes.expect(has_properties(composer='Composer'))
        self.driver.changeComposer('Composer')
        self.check(changes)

        changes.expect(has_properties(publisher='Publisher'))
        self.driver.changePublisher('Publisher')
        self.check(changes)

        changes.expect(has_properties(isrc='ZZZ123456789'))
        self.driver.changeIsrc('ZZZ123456789')
        self.check(changes)

        changes.expect(has_properties(tags='Tag1 Tag2 Tag3'))
        self.driver.changeTags('Tag1 Tag2 Tag3')
        self.check(changes)

        changes.expect(has_properties(lyrics='Lyrics\n...\n'))
        self.driver.addLyrics('Lyrics')
        self.driver.addLyrics('...')
        self.check(changes)

        changes.expect(has_properties(language='eng'))
        self.driver.changeLanguage('eng')
        self.check(changes)