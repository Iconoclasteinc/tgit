# -*- coding: utf-8 -*-

import shutil
from tempfile import NamedTemporaryFile
import unittest

from hamcrest import *

import mutagen.mp3 as mp3
import mutagen.id3 as id3

from tests.util import project

from tgit.mp3 import MP3File

ALBUM_TITLE = "Album Title"
ALBUM_ARTIST = "Album Artist"
TRACK_TITLE = "Track Title"
BITRATE_IN_BPS = 320000
BITRATE_IN_KBPS = 320
DURATION_IN_S = 9.064475
DURATION_AS_TEXT = "00:09"


class MP3FileTest(unittest.TestCase):
    def setUp(self):
        self._create_test_mp3(album=ALBUM_TITLE, artist=ALBUM_ARTIST, track=TRACK_TITLE)
        self.audio = MP3File(self.working_file.name)

    def tearDown(self):
        self._delete_test_mp3()

    def test_reads_album_title_from_id3_tags(self):
        assert_that(self.audio.album_title, equal_to(ALBUM_TITLE), "album title")

    def test_reads_album_artist_from_id3_tags(self):
        assert_that(self.audio.album_artist, equal_to(ALBUM_ARTIST), "album artist")

    def test_reads_track_title_from_id3_tags(self):
        assert_that(self.audio.track_title, equal_to(TRACK_TITLE), "track title")

    def test_reads_track_bitrate_from_audio_stream_information(self):
        assert_that(self.audio.bitrate, equal_to(BITRATE_IN_BPS), "bitrate")

    def test_can_report_bitrate_rounded_in_kbps(self):
        assert_that(self.audio.bitrate_in_kbps, equal_to(BITRATE_IN_KBPS),
                    "bitrate in kbps")

    def test_reads_track_duration_from_audio_stream_information(self):
        assert_that(self.audio.duration, equal_to(DURATION_IN_S), "duration")

    def test_can_report_duration_as_human_readable_text(self):
        assert_that(self.audio.duration_as_text, equal_to(DURATION_AS_TEXT),
                    "duration as text")

    # todo introduce a matcher for comparing all metadata
    # something like assert_that(modified_audio, same_metada_as(original_audio))
    def test_saves_metadata_back_to_audio_file(self):
        self.audio.album_title = "Modified Album Title"
        self.audio.album_artist = "Modified Album Artist"
        self.audio.track_title = "Modified Track Title"
        self.audio.save()

        modified_audio = MP3File(self.working_file.name)
        assert_that(modified_audio.album_title, equal_to("Modified Album Title"),
                    "modified album title")
        assert_that(modified_audio.album_artist, equal_to("Modified Album Artist"),
                    "modified album artist")
        assert_that(modified_audio.track_title, equal_to("Modified Track Title"),
                    "modified track title")

    def _create_test_mp3(self, **tags):
        self._copy_master(project.test_resource_path('base.mp3'))
        self._populate_tags(tags)

    def _copy_master(self, master_file):
        self.working_file = NamedTemporaryFile(suffix='.mp3')
        shutil.copy(master_file, self.working_file.name)

    def _populate_tags(self, tags):
        test_mp3 = mp3.MP3(self.working_file.name)
        test_mp3.add_tags()
        test_mp3.tags.add(id3.TALB(encoding=3, text=tags['album']))
        test_mp3.tags.add(id3.TPE1(encoding=3, text=tags['artist']))
        test_mp3.tags.add(id3.TIT2(encoding=3, text=tags['track']))
        test_mp3.save()

    def _delete_test_mp3(self):
        self.working_file.close()