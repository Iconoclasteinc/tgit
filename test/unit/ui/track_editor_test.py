# -*- coding: utf-8 -*-
import unittest
from flexmock import flexmock
from hamcrest import assert_that, equal_to
from test.util import builders as build
from tgit.ui.track_editor import TrackEditor
from tgit.ui.views.track_page import TrackPage

ANY_POSITION = 0


class TrackEditorTest(unittest.TestCase):

    def setUp(self):
        self.album, self.track = build.album(), build.track()
        self.editor = TrackEditor(self.album, self.track)

    def testUpdatesTrackMetadataOnEdition(self):
        class Snapshot(object):
            pass

        state = Snapshot()
        state.trackTitle = 'Title'
        state.versionInfo = 'Version'
        state.featuredGuest = 'Featuring'
        state.lyricist = 'Lyricist'
        state.composer = 'Composer'
        state.publisher = 'Publisher'
        state.isrc = 'ZZZ123456789'
        state.tags = 'Tags'
        state.lyrics = 'Lyrics\nLyrics\n...'
        state.language = 'und'

        self.editor.metadataEdited(state)

        assert_that(self.track.trackTitle, equal_to('Title'), 'track title')
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
        flexmock(TrackPage).should_receive('show').with_args(self.album, self.track).once()
        self.editor.trackStateChanged(self.track)

    def testRefreshesPageWhenTracksAreRemovedFromAlbum(self):
        otherTrack = build.track()
        flexmock(TrackPage).should_receive('show').with_args(self.album, self.track).once()
        self.editor.trackRemoved(otherTrack, position=ANY_POSITION)

    def testRefreshesPageWhenTracksAreAddedToAlbum(self):
        otherTrack = build.track()
        flexmock(TrackPage).should_receive('show').with_args(self.album, self.track).once()
        self.editor.trackAdded(otherTrack, position=ANY_POSITION)

    def testStopsRefreshingPageAfterTrackRemoval(self):
        self.album.addAlbumListener(self.editor)
        self.track.addTrackListener(self.editor)
        flexmock(TrackPage).should_receive('show').never()

        self.editor.trackRemoved(self.track, position=ANY_POSITION)
        self.album.addTrack(build.track())
        self.track.trackTitle = 'Updated title'