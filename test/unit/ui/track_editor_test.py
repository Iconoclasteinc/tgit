# -*- coding: utf-8 -*-
import unittest
from hamcrest import assert_that, equal_to, same_instance
from test.util import builders as build
from tgit.ui.track_editor import TrackEditor


class TrackViewStub(object):
    def __init__(self):
        self.timesDisplayed = 0
        self.handlers = {}

    def __getattr__(self, item):
        if item not in self.handlers:
            raise AssertionError('No handler bound to event : ' + item)

        return self.handlers[item]

    def bind(self, **handlers):
        self.handlers.update(handlers)

    def display(self, track):
        self.timesDisplayed += 1
        self.track = track


class TrackEditorTest(unittest.TestCase):
    def setUp(self):
        # Make sure album metadata is not empty to avoid triggering a change event when
        # first track is added to album
        self.album = build.album(releaseName='Title')
        self.track = build.track()
        self.album.addTrack(self.track)
        self.view = TrackViewStub()
        self.editor = TrackEditor(self.track, self.view)

    def testDisplaysTrackWhenRendered(self):
        view = self.editor.render()
        assert_that(view, same_instance(self.view), 'view')
        assert_that(self.view.track, equal_to(self.track), 'displayed track')

    def testUpdatesTrackOnEdition(self):
        class Snapshot(object):
            pass

        changes = Snapshot()
        changes.trackTitle = 'Title'
        changes.leadPerformer = 'Artist'
        changes.versionInfo = 'Version'
        changes.featuredGuest = 'Featuring'
        changes.lyricist = 'Lyricist'
        changes.composer = 'Composer'
        changes.publisher = 'Publisher'
        changes.isrc = 'ZZZ123456789'
        changes.tags = 'Tags'
        changes.lyrics = 'Lyrics\nLyrics\n...'
        changes.language = 'und'

        self.view.metadataChanged(changes)

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
        self.track.trackTitle = 'changed'
        assert_that(self.view.timesDisplayed, equal_to(1), 'refresh count')

    def testRefreshesPageOnAlbumCompositionChange(self):
        other = build.track()
        self.album.addTrack(other)
        assert_that(self.view.timesDisplayed, equal_to(1), 'refresh count after addition')

        self.album.removeTrack(other)
        assert_that(self.view.timesDisplayed, equal_to(2), 'refresh count after removal')

    def testStopsRefreshingPageOnceTrackRemovedFromAlbum(self):
        self.album.removeTrack(self.track)
        assert_that(self.view.timesDisplayed, equal_to(0), 'refresh count after removal')

        self.track.trackTitle = 'changed'
        assert_that(self.view.timesDisplayed, equal_to(0), 'refresh count after change')