# -*- coding: utf-8 -*-
import unittest
from flexmock import flexmock
from hamcrest import has_property, match_equality
from test.util import builders as build, fakes
from tgit.ui.album_director import AlbumDirector


class AlbumDirectorTest(unittest.TestCase):
    def setUp(self):
        self.album = build.album()
        self.catalog = flexmock()
        self.director = AlbumDirector(self.album, self.catalog, fakes.audioPlayer())

    def testSavesAllTracksInAlbum(self):
        self.album.addTrack(build.track(trackTitle='first'))
        self.album.addTrack(build.track(trackTitle='second'))
        self.album.addTrack(build.track(trackTitle='third'))

        self.catalog.should_receive('save').with_args(hasTitle('first')).once()
        self.catalog.should_receive('save').with_args(hasTitle('second')).once()
        self.catalog.should_receive('save').with_args(hasTitle('third')).once()

        self.director.recordAlbum()


def hasTitle(title):
    return match_equality(has_property('trackTitle', title))
