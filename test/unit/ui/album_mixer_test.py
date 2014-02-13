# -*- coding: utf-8 -*-
import unittest
from hamcrest import assert_that, contains, has_properties
from test.util import builders as build, resources, fakes
from tgit.ui.album_mixer import AlbumMixer


def audioFolder():
    return resources.path('audio')


def audioFile(audio):
    return resources.path('audio', audio)


class AlbumMixerTest(unittest.TestCase):
    def setUp(self):
        self.album = build.album()
        self.library = fakes.trackLibrary()
        self.mixer = AlbumMixer(self.album, self.library)

    def populateTrackCatalog(self):
        self.library.add(build.track(filename=audioFile('1.mp3'), trackTitle='first'))
        self.library.add(build.track(filename=audioFile('2.mp3'), trackTitle='second'))
        self.library.add(build.track(filename=audioFile('3.mp3'), trackTitle='third'))

    def testAddsSelectedTracksToAlbumInSelectionOrder(self):
        self.populateTrackCatalog()

        self.mixer.tracksSelected([audioFile('1.mp3'), audioFile('3.mp3'), audioFile('2.mp3')])

        assert_that(self.album.tracks, contains(
            has_properties(trackTitle='first'),
            has_properties(trackTitle='third'),
            has_properties(trackTitle='second')))

    def testAddsAllTracksInSelectedFolder(self):
        self.populateTrackCatalog()

        self.mixer.tracksSelected([audioFolder()])

        assert_that(self.album.tracks, contains(
            has_properties(trackTitle='first'),
            has_properties(trackTitle='second'),
            has_properties(trackTitle='third')))