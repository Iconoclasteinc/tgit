# -*- coding: utf-8 -*-
import unittest
from flexmock import flexmock
from hamcrest import assert_that, equal_to
from test.util import builders as build
from tgit.ui.track_editor import TrackEditor


class PageStub(object):
    def onMetadataChange(self, callback):
        self.callback = callback

    def updateTrack(self, track, album):
        self.track = track
        self.album = album

    def clear(self):
        self.track = None
        self.album = None

    def triggerChange(self, state):
        self.callback(state)


class TrackEditorTest(unittest.TestCase):
    def setUp(self):
        self.album, self.track = build.album(), build.track()
        self.album.addTrack(self.track)
        self.editor = TrackEditor(self.album, self.track)

    def testUpdatesPagesWhenAdded(self):
        page = PageStub()
        self.editor.add(page)

        assert_that(page.track, equal_to(self.track), 'page track')
        assert_that(page.album, equal_to(self.album), 'page album')

    def testUpdatesTrackMetadataOnEdition(self):
        page = PageStub()
        self.editor.add(page)

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

        page.triggerChange(state)

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
        page = flexmock(PageStub())
        self.editor.add(page)

        page.should_receive('updateTrack').with_args(self.track, self.album).at_least().once()
        self._triggerTrackChange()

    def testRefreshesPageWhenAlbumCompositionChanges(self):
        page = flexmock(PageStub())
        self.editor.add(page)

        flexmock(page).should_receive('updateTrack').with_args(self.track, self.album).at_least().times(2)

        other = build.track()
        self.album.addTrack(other)
        self.album.removeTrack(other)

    def testStopsRefreshingPageAfterTrackRemoval(self):
        page = flexmock(PageStub())
        self.editor.add(page)

        flexmock(page).should_receive('updateTrack').with_args(self.track, self.album).never()

        self.album.removeTrack(self.track)
        self._triggerTrackChange()

    def _triggerTrackChange(self):
        self.track.trackTitle = 'change'

