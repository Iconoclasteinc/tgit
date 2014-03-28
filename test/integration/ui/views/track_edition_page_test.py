# -*- coding: utf-8 -*-

from datetime import timedelta
from hamcrest import has_properties, contains_string

from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe
from test.drivers import TrackEditionPageDriver
from test.integration.ui.views import ViewTest
from test.util import builders as build

from tgit.ui.views.track_edition_page import TrackEditionPage


class TrackEditionPageTest(ViewTest):
    def setUp(self):
        super(TrackEditionPageTest, self).setUp()
        self.page = TrackEditionPage()
        self.driver = self.createDriverFor(self.page)
        self.show(self.page)

    def createDriverFor(self, widget):
        return TrackEditionPageDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysAlbumSummaryInBanner(self):
        album = build.album(releaseName='Album Title', leadPerformer='Artist', labelName='Record Label')
        track = build.track()
        album.addTrack(build.track())
        album.addTrack(track)
        album.addTrack(build.track())

        self.page.display(track)
        self.driver.showsAlbumTitle('Album Title')
        self.driver.showsAlbumLeadPerformer('Artist')
        self.driver.showsAlbumLabel('Record Label')
        self.driver.showsTrackNumber(contains_string('2 of 3'))

    def testIndicatesWhenAlbumPerformedByVariousArtists(self):
        album = build.album(compilation=True)
        track = build.track()
        album.addTrack(track)

        self.page.display(track)
        self.driver.showsAlbumLeadPerformer('Various Artists')

    def testDisplaysTrackMetadata(self):
        album = build.album()
        track = build.track(bitrate=192000,
                            compilation=True,
                            duration=timedelta(minutes=4, seconds=35).total_seconds(),
                            leadPerformer='Artist',
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
        album.addTrack(track)

        self.page.display(track)

        self.driver.showsTrackTitle('Song')
        self.driver.showsLeadPerformer('Artist')
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
        album = build.album(compilation=False, leadPerformer='Album Artist')
        track = build.track()
        album.addTrack(track)

        self.page.display(track)
        self.driver.showsLeadPerformer('Album Artist', disabled=True)

    def testSignalsWhenTrackMetadataEdited(self):
        changes = ValueMatcherProbe('track changed')
        self.page.onMetadataChange(changes.received)

        changes.expect(has_properties(trackTitle='Title'))
        self.driver.changeTrackTitle('Title')
        self.check(changes)

        changes.expect(has_properties(leadPerformer='Artist'))
        self.driver.changeLeadPerformer('Artist')
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

        changes.expect(has_properties(language='fra'))
        self.driver.selectLanguage('fra')
        self.check(changes)

    def testDisplaysSoftwareNoticeInLocalTime(self):
        album = build.album()
        track = build.track(tagger='TGiT v1.0', taggingTime='2014-03-23 20:33:00 +0000')
        album.addTrack(track)

        self.page.display(track)

        # This will likely fail when ran on another timezone or even when daylight savings
        # change, but I don't yet know how to best write the test
        self.driver.showsSoftwareNotice('Tagged with TGiT v1.0 on 2014-03-23 at 16:33:00')

    def testOmitsSoftwareNoticeIfTaggerInformationUnavailable(self):
        album = build.album()
        track = build.track(taggingTime='2014-03-23 20:33:00 UTC+0000')
        album.addTrack(track)

        self.page.display(track)
        self.driver.showsSoftwareNotice('')

    def testOmitsSoftwareNoticeIfTaggingDateMalformed(self):
        album = build.album()
        track = build.track(tagger='TGiT v1.0', taggingTime='@$%@#$%#@$%#@%#@$')
        album.addTrack(track)

        self.page.display(track)
        self.driver.showsSoftwareNotice('')