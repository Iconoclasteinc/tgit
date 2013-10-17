# -*- coding: utf-8 -*-

import unittest
from hamcrest import assert_that, contains, has_property
from flexmock import flexmock

from tgit.producer import AlbumProducer
from tgit.album import Album
from tgit.mp3_file import MP3File
from tgit.null import Null


class AlbumProducerTest(unittest.TestCase):
    def setUp(self):
        self.library = flexmock(load=lambda filename: MP3File(filename))
        self.album = Album()
        self.producer = AlbumProducer(Null(), self.album, self.library)

    def testLoadsAudioFileAndAddsTrackToAlbum(self):
        self.producer.addTrack('name of file')
        assert_that(self.album.tracks, contains(has_property('filename', 'name of file')),
                    'tracks in album')
