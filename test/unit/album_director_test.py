# -*- coding: utf-8 -*-

import unittest

from hamcrest import assert_that, contains, has_properties, has_entries, is_not, has_key

from test.util import builders as build

from tgit.album_director import AlbumDirector


class InMemoryMetadataStore(object):
    def __init__(self):
        self.storage = {}

    def __getitem__(self, key):
        return self.storage[key]

    def __setitem__(self, key, metadata):
        self.storage[key] = metadata

    def load(self, key):
        return self[key]

    def save(self, key, metadata):
        self[key] = metadata


class AlbumDirectorTest(unittest.TestCase):
    def setUp(self):
        self.store = InMemoryMetadataStore()
        self.director = AlbumDirector(self.store)

    def testLoadsMetadataAndAddsTracksToAlbumInOrder(self):
        self.store['my favorite things'] = build.metadata(trackTitle='My Favorite Things')
        self.store['summertime'] = build.metadata(trackTitle='Summertime')

        album = build.album()
        self.director.addTrack(album, 'my favorite things')
        self.director.addTrack(album, 'summertime')

        assert_that(album.tracks, contains(
            has_properties(filename='my favorite things', trackTitle='My Favorite Things'),
            has_properties(filename='summertime', trackTitle='Summertime')), 'album tracks')

    def testSavesAlbumInTracksMetadata(self):
        myFavoriteThings = build.album(releaseName='My Favorite Things')

        myFavoriteThings.addTrack(build.track(filename='everytime we say goodbye',
                                              trackTitle='Everytime We Say Goodbye'))
        myFavoriteThings.addTrack(build.track(filename='but not for me',
                                              trackTitle='But Not For Me'))

        self.director.recordAlbum(myFavoriteThings)

        assert_that(self.store['everytime we say goodbye'],
                    has_entries(releaseName='My Favorite Things',
                                trackTitle='Everytime We Say Goodbye'),
                    'everytime we say goodbye')
        assert_that(self.store['but not for me'],
                    has_entries(releaseName='My Favorite Things',
                                trackTitle='But Not For Me'),
                    'but not for me')