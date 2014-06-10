# -*- coding: utf-8 -*-
import unittest
from hamcrest import assert_that, contains, has_properties
from test.util import builders as build, resources, doubles
from tgit.ui.album_mixer import AlbumMixer


def audioFolder():
    return resources.path('audio')


def audioFile(audio):
    return resources.path('audio', audio)


class TrackSelectorStub(object):
    def __init__(self):
        self.selectedTracks = []
        self.handlers = {}

    def __getattr__(self, item):
        if item not in self.handlers:
            raise AssertionError('No handler bound to event : ' + item)
        return self.handlers[item]

    def show(self, folders):
        self.tracksSelected(self.selectedTracks)

    def bind(self, **handlers):
        self.handlers.update(handlers)


class AlbumMixerTest(unittest.TestCase):
    def setUp(self):
        self.album = build.album()
        self.library = doubles.trackLibrary()
        self.tracksSelector = TrackSelectorStub()
        self.mixer = AlbumMixer(self.album, self.library, self.tracksSelector)
        self.populateTrackCatalog()

    def populateTrackCatalog(self):
        self.library.store(build.track(filename=audioFile('1.mp3'), trackTitle='first'))
        self.library.store(build.track(filename=audioFile('2.mp3'), trackTitle='second'))
        self.library.store(build.track(filename=audioFile('3.mp3'), trackTitle='third'))

    def testAddsSelectedTracksToAlbumInSelectionOrder(self):
        self.tracksSelector.selectedTracks = [audioFile('1.mp3'), audioFile('3.mp3'), audioFile('2.mp3')]

        self.mixer.select(album=False)
        assert_that(self.album.tracks, contains(
            has_properties(trackTitle='first'),
            has_properties(trackTitle='third'),
            has_properties(trackTitle='second')))

    def testAddsAllTracksInSelectedFolder(self):
        self.tracksSelector.selectedTracks = [audioFolder()]

        self.mixer.select(album=True)
        assert_that(self.album.tracks, contains(
            has_properties(trackTitle='first'),
            has_properties(trackTitle='second'),
            has_properties(trackTitle='third')))