# -*- coding: utf-8 -*-
import unittest
from hamcrest import assert_that, equal_to
from test.util import builders as build
from tgit.ui.track_editor import TrackEditor


class PageStub(object):
    def __init__(self):
        self.refreshCount = 0

    def onMetadataChange(self, callback):
        self.metadataChange = callback

    def updateTrack(self, track, album):
        self.refreshCount += 1
        self.track = track
        self.album = album


class TrackEditorTest(unittest.TestCase):
    def setUp(self):
        self.album, self.track = build.album(), build.track()
        self.album.addTrack(self.track)
        self.page = PageStub()
        self.editor = TrackEditor(self.album, self.track, self.page)

    def testUpdatesPageWhenAdded(self):
        assert_that(self.page.track, equal_to(self.track), 'page track')
        assert_that(self.page.album, equal_to(self.album), 'page album')

    def testUpdatesTrackMetadataOnEdition(self):
        class Snapshot(object):
            pass

        state = Snapshot()
        state.trackTitle = 'Title'
        state.leadPerformer = 'Artist'
        state.versionInfo = 'Version'
        state.featuredGuest = 'Featuring'
        state.lyricist = 'Lyricist'
        state.composer = 'Composer'
        state.publisher = 'Publisher'
        state.isrc = 'ZZZ123456789'
        state.tags = 'Tags'
        state.lyrics = 'Lyrics\nLyrics\n...'
        state.language = 'und'

        self.page.metadataChange(state)

        assert_that(self.track.trackTitle, equal_to('Title'), 'track title')
        assert_that(self.track.leadPerformer, equal_to('Artist'), 'lead performer')
        assert_that(self.track.versionInfo, equal_to('Version'), 'version info')
        assert_that(self.track.featuredGuest, equal_to('Featuring'), 'featured guest')
        assert_that(self.track.lyricist, equal_to('Lyricist'), 'lyricist')
        assert_that(self.track.composer, equal_to('Composer'), 'composer')
        assert_that(self.track.publisher, equal_to('Publisher'), 'publisher')
        assert_that(self.track.isrc, equal_to('ZZZ123456789'), 'isrc')
        assert_that(self.track.tags, equal_to('Tags'), 'tags')
        assert_that(self.track.lyrics, equal_to('Lyrics\nLyrics\n...'), 'lyrics')
        assert_that(self.track.language, equal_to('und'), 'language')

    def testRefreshesPageOnTrackChange(self):
        self.page.refreshCount = 0
        self.track.trackTitle = 'changed'
        assert_that(self.page.refreshCount, equal_to(1), "refresh count")

    def testRefreshesPageWhenAlbumCompositionChanges(self):
        other = build.track()
        self.album.addTrack(other)

        self.page.refreshCount = 0
        self.album.removeTrack(other)
        assert_that(self.page.refreshCount, equal_to(1), "refresh count")

    def testStopsRefreshingPageAfterTrackRemoval(self):
        self.album.removeTrack(self.track)

        self.page.refreshCount = 0
        self.track.trackTitle = 'changed'
        assert_that(self.page.refreshCount, equal_to(0), "refresh count")


