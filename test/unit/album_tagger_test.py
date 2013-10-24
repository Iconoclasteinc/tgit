# -*- coding: utf-8 -*-

import unittest

from hamcrest import assert_that, contains, has_property
from flexmock import flexmock

from tgit.producer import AlbumTagger
from tgit.album import Album
from tgit.mp3_file import MP3File


class AlbumTaggerTest(unittest.TestCase):

    def setUp(self):
        self.library = flexmock(load=lambda filename: MP3File(filename))
        self.album = flexmock(Album())
        self.producer = AlbumTagger(self.album, self.library)

    def testLoadsAudioFileAndAddsTrackToAlbum(self):
        self.producer.importTrack('name of file')
        assert_that(self.album.tracks, contains(has_property('filename', 'name of file')),
                    'tracks in album')

    def testTagsAlbumWhenRecorded(self):
        self.album.should_receive('tag').once()
        self.producer.recordAlbum()