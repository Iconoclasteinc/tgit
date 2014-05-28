# -*- coding: utf-8 -*-
import unittest
from flexmock import flexmock
from hamcrest import has_property, match_equality
from test.util import builders as build, fakes
from tgit.ui.album_director import AlbumDirector


class AlbumViewStub(object):
    def __init__(self):
        self.refreshCount = 0
        self.handlers = {}
        self.tracks = []

    def __getattr__(self, item):
        if item not in self.handlers:
            raise AssertionError('No handler bound to event : ' + item)

        return self.handlers[item]

    def bind(self, **handlers):
        self.handlers.update(handlers)

    def addTrackEditionPage(self, page, position):
        self.tracks.insert(position, page)

    def allowSaves(self, allow):
        self.saveEnabled = allow

    def display(self, album):
        self.album = album
        self.refreshCount += 1


class TrackViewStub(object):
    def __init__(self, track):
        self.track = track


class AlbumDirectorTest(unittest.TestCase):
    def setUp(self):
        self.album = build.album()
        self.catalog = flexmock()
        self.view = AlbumViewStub()
        self.director = AlbumDirector(self.album, self.catalog, fakes.audioPlayer(), self.view, TrackViewStub)

    def testSavesAllTracksInAlbum(self):
        self.album.addTrack(build.track(trackTitle='first'))
        self.album.addTrack(build.track(trackTitle='second'))
        self.album.addTrack(build.track(trackTitle='third'))

        self.catalog.should_receive('store').with_args(hasTitle('first')).once()
        self.catalog.should_receive('store').with_args(hasTitle('second')).once()
        self.catalog.should_receive('store').with_args(hasTitle('third')).once()

        self.view.recordAlbum()


def hasTitle(title):
    return match_equality(has_property('trackTitle', title))
