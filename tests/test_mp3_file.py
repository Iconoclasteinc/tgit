# -*- coding: utf-8 -*-

import unittest
import shutil
from tempfile import NamedTemporaryFile

from hamcrest import *

import mutagen.mp3 as mp3
import mutagen.id3 as id3

import project

from tgit.mp3 import MP3File


class MP3FileTest(unittest.TestCase):
    def setUp(self):
        self._create_test_mp3(album="Titre de l'album")
        self.audio = MP3File(self.working_file.name)

    def tearDown(self):
        self._delete_test_mp3()

    def test_reads_album_title_from_id3_tags(self):
        assert_that(self.audio.album_title, equal_to("Titre de l'album"), "album title")

    def _create_test_mp3(self, album):
        self._copy_master(project.test_resource_path('base.mp3'))
        self._populate_tags(album)

    def _copy_master(self, master_file):
        self.working_file = NamedTemporaryFile(suffix='.mp3')
        shutil.copy(master_file, self.working_file.name)

    def _populate_tags(self, album):
        test_mp3 = mp3.MP3(self.working_file.name)
        test_mp3.tags.add(id3.TALB(encoding=3, text=album))
        test_mp3.save()

    def _delete_test_mp3(self):
        self.working_file.close()


if __name__ == '__main__':
    unittest.main()
