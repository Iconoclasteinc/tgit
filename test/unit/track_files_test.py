# -*- coding: utf-8 -*-

import unittest
from flexmock import flexmock
from hamcrest import assert_that, all_of, has_property, equal_to

from test.util import builders as build

from tgit.metadata import Metadata
from tgit import tags
from tgit.mp3.track_files import TrackFiles


class TrackFilesTest(unittest.TestCase):
    def setUp(self):
        self.container = flexmock()
        self.catalog = TrackFiles(self.container)

    def merge(self, *metadata):
        merge = Metadata()
        for data in metadata:
            merge.merge(data)
        return merge

    def testLoadsAlbumAndTrackMetadataFromContainer(self):
        metadata = build.metadata(trackTitle='Summertime',
                                  releaseName='My Favorite Things',
                                  images=[('image/jpeg', 'Front Cover', 'data')])

        self.container.should_receive('load').with_args('summertime.mp3').and_return(metadata)

        track = self.catalog.load('summertime.mp3')

        assert_that(track, hasTrackMetadata(metadata), 'track metadata')
        assert_that(track.album, hasAlbumMetadata(metadata), 'album metadata')

    def testSavesAlbumAndTrackMetadataToContainer(self):
        track = build.track(filename='summertime.mp3',
                            trackTitle='Summertime')
        album = build.album(releaseName='My Favorite Things',
                            images=[build.image('image/jpeg', 'data', 'Front Cover')])
        track.album = album

        self.container.should_receive('save').\
            with_args('summertime.mp3', self.merge(track.metadata, album.metadata)).once()

        self.catalog.save(track)


def hasTrackMetadata(metadata):
    return all_of(*[has_property(tag, metadata[tag]) for tag in tags.TRACK_TAGS])


def hasAlbumMetadata(metadata):
    matchers = [has_property(tag, metadata[tag]) for tag in tags.ALBUM_TAGS]
    matchers.append(has_property('images', equal_to(metadata.images)))
    return all_of(*matchers)
