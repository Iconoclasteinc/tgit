# -*- coding: utf-8 -*-

from datetime import timedelta

from hamcrest import contains_string, has_entries

from cute.finders import WidgetIdentity
from cute.probes import ValueMatcherProbe
from test.drivers.track_edition_page_driver import TrackEditionPageDriver
from test.integration.ui import WidgetTest
from test.util import builders as build
from tgit.ui.track_edition_page import TrackEditionPage


class TrackEditionPageTest(WidgetTest):
    def render(self, album, track):
        self.page = TrackEditionPage(album, track)
        self.page.display(album, track)
        self.driver = self.createDriverFor(self.page)
        self.show(self.page)

    def createDriverFor(self, widget):
        return TrackEditionPageDriver(WidgetIdentity(widget), self.prober, self.gesture_performer)

    def testDisplaysAlbumSummaryInBanner(self):
        track = build.track()
        album = build.album(release_name='Album Title', lead_performer='Artist', label_name='Record Label',
                            tracks=[build.track(), track, build.track()])

        self.render(album, track)

        self.driver.showsAlbumTitle('Album Title')
        self.driver.shows_album_lead_performer('Artist')
        self.driver.showsAlbumLabel('Record Label')
        self.driver.showsTrackNumber(contains_string('2 of 3'))

    def testIndicatesWhenAlbumPerformedByVariousArtists(self):
        track = build.track()
        album = build.album(compilation=True, tracks=[track])
        self.render(album, track)
        self.driver.shows_album_lead_performer('Various Artists')

    def testDisplaysTrackMetadata(self):
        track = build.track(bitrate=192000,
                            duration=timedelta(minutes=4, seconds=35).total_seconds(),
                            lead_performer='Artist',
                            track_title='Song',
                            versionInfo='Remix',
                            featuredGuest='Featuring',
                            lyricist='Lyricist',
                            composer='Composer',
                            publisher='Publisher',
                            isrc='Code',
                            labels='Tag1 Tag2 Tag3',
                            lyrics='Lyrics\n...\n...',
                            language='eng')
        album = build.album(compilation=True, tracks=[track])

        self.render(album, track)

        self.driver.showsTrackTitle('Song')
        self.driver.shows_lead_performer('Artist')
        self.driver.showsVersionInfo('Remix')
        self.driver.showsBitrate('192 kbps')
        self.driver.showsDuration('04:35')
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

    def testDisablesLeadPerformerEditionWhenAlbumIsNotACompilation(self):
        track = build.track()
        album = build.album(lead_performer='Album Artist', compilation=False, tracks=[track])
        self.render(album, track)
        self.driver.shows_lead_performer('Album Artist', disabled=True)

    def testSignalsWhenTrackMetadataChange(self):
        track = build.track()
        album = build.album(compilation=True, tracks=[track])

        self.render(album, track)

        metadataChangedSignal = ValueMatcherProbe('metadata changed')
        self.page.metadataChanged.connect(metadataChangedSignal.received)

        metadataChangedSignal.expect(has_entries(track_title='Title'))
        self.driver.changeTrackTitle('Title')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(lead_performer='Artist'))
        self.driver.change_lead_performer('Artist')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(versionInfo='Remix'))
        self.driver.changeVersionInfo('Remix')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(featuredGuest='Featuring'))
        self.driver.changeFeaturedGuest('Featuring')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(lyricist='Lyricist'))
        self.driver.changeLyricist('Lyricist')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(composer='Composer'))
        self.driver.changeComposer('Composer')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(publisher='Publisher'))
        self.driver.changePublisher('Publisher')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(isrc='ZZZ123456789'))
        self.driver.changeIsrc('ZZZ123456789')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(labels='Tag1 Tag2 Tag3'))
        self.driver.changeTags('Tag1 Tag2 Tag3')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(lyrics='Lyrics\n...\n'))
        self.driver.addLyrics('Lyrics')
        self.driver.addLyrics('...')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(language='eng'))
        self.driver.changeLanguage('eng')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(language='fra'))
        self.driver.selectLanguage('fra')
        self.check(metadataChangedSignal)

    def testDisplaysSoftwareNoticeInLocalTime(self):
        track = build.track(tagger='TGiT v1.0', taggingTime='2014-03-23 20:33:00 +0000')
        album = build.album(tracks=[track])

        self.render(album, track)

        # This will likely fail when ran on another timezone or even when daylight savings
        # change, but I don't yet know how to best write the test

        # edit: use renderAsOf(track, dateFormat)
        self.driver.showsSoftwareNotice('Tagged with TGiT v1.0 on 2014-03-23 at 16:33:00')

    def testOmitsSoftwareNoticeIfTaggerInformationUnavailable(self):
        track = build.track(taggingTime='2014-03-23 20:33:00 UTC+0000')
        album = build.album(tracks=[track])
        self.render(album, track)
        self.driver.showsSoftwareNotice('')

    def testOmitsSoftwareNoticeIfTaggingDateMalformed(self):
        track = build.track(tagger='TGiT v1.0', taggingTime='invalid-time-format')
        album = build.album(tracks=[track])
        self.render(album, track)
        self.driver.showsSoftwareNotice('')