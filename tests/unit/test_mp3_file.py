# -*- coding: utf-8 -*-

import shutil
from tempfile import NamedTemporaryFile
import unittest

from hamcrest import *

import mutagen.mp3 as mp3
import mutagen.id3 as id3

from tests.util import project

from tgit.mp3 import MP3File

SAMPLE_MP3_FILE = project.test_resource_path("base.mp3")
FRONT_COVER_PICTURE_FILE = project.test_resource_path("front-cover-sample.jpg")
OTHER_FRONT_COVER_PICTURE_FILE = project.test_resource_path("banana-song-cover.png")
BACK_COVER_PICTURE_FILE = project.test_resource_path("back-cover-sample.jpg")

RELEASE_NAME = "Release Name"
LEAD_PERFORMER = "Lead Performer"
ORIGINAL_RELEASE_DATE = "2013-11-15"
TRACK_TITLE = "Track Title"
VERSION_INFO = "Version Info"
BITRATE_IN_BPS = 320000
BITRATE_IN_KBPS = 320
DURATION_IN_S = 9.064475
DURATION_AS_TEXT = "00:09"


def image_data(filename):
    return open(filename).read()


class MP3FileTest(unittest.TestCase):
    def setUp(self):
        self._create_test_mp3(release_name=RELEASE_NAME,
                              front_cover_picture=('image/jpeg', FRONT_COVER_PICTURE_FILE),
                              back_cover_picture=('image/jpeg', BACK_COVER_PICTURE_FILE),
                              lead_performer=LEAD_PERFORMER,
                              original_release_date=ORIGINAL_RELEASE_DATE,
                              track_title=TRACK_TITLE,
                              version_info=VERSION_INFO)
        self.audio = MP3File(self.working_file.name)

    def tearDown(self):
        self._delete_test_mp3()


    @unittest.skip("pending")
    def test_creates_mp3_tags_when_missing(self):
        self.fail("Not implemented")

    def test_reads_release_name_from_id3_tags(self):
        assert_that(self.audio.release_name, equal_to(RELEASE_NAME), "release name")

    def test_reads_front_cover_picture_from_id3_tags(self):
        assert_that(len(self.audio.front_cover_picture),
                    equal_to(len(image_data(FRONT_COVER_PICTURE_FILE))),
                    "front cover picture size in bytes")

    @unittest.skip("Pending")
    def test_records_a_single_front_cover_picture(self):
        self.fail("Not implemented")
        # test with a front cover without a description
        # test with a front cover with the same description

    @unittest.skip("Pending")
    def test_leaves_other_attached_pictures_unchanged(self):
        self.fail("Not implemented")
        # test with a other attached pictures with or without a description

    def test_reads_lead_performer_from_id3_tags(self):
        assert_that(self.audio.lead_performer, equal_to(LEAD_PERFORMER), "lead performer")

    def test_reads_original_release_date_from_id3_tags(self):
        assert_that(self.audio.original_release_date, equal_to(ORIGINAL_RELEASE_DATE),
                    "original release date")

    def test_reads_track_title_from_id3_tags(self):
        assert_that(self.audio.track_title, equal_to(TRACK_TITLE), "track title")

    def test_reads_version_info_from_id3_tags(self):
        assert_that(self.audio.version_info, equal_to(VERSION_INFO), "version info")

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
    # then test round tripping on several test data samples
    def test_saves_metadata_back_to_audio_file(self):
        self.audio.release_name = "Modified Release Name"
        self.audio.front_cover_picture = 'image/png', image_data(OTHER_FRONT_COVER_PICTURE_FILE)
        self.audio.lead_performer = "Modified Lead Performer"
        self.audio.original_release_date = "2013-12-01"
        self.audio.track_title = "Modified Track Title"
        self.audio.version_info = "Modified Version Info"
        self.audio.save()

        modified_audio = MP3File(self.working_file.name)
        assert_that(modified_audio.release_name, equal_to("Modified Release Name"),
                    "modified release name")
        assert_that(len(modified_audio.front_cover_picture),
                    equal_to(len(image_data(OTHER_FRONT_COVER_PICTURE_FILE))),
                    "modified front cover picture size in bytes")
        assert_that(modified_audio.lead_performer, equal_to("Modified Lead Performer"),
                    "modified lead performer")
        assert_that(modified_audio.original_release_date, equal_to("2013-12-01"),
                    "modified original release date")
        assert_that(modified_audio.track_title, equal_to("Modified Track Title"),
                    "modified track title")
        assert_that(modified_audio.version_info, equal_to("Modified Version Info"),
                    "modified version info")

    def _create_test_mp3(self, **tags):
        self._copy_master(SAMPLE_MP3_FILE)
        self._populate_tags(tags)

    def _copy_master(self, master_file):
        self.working_file = NamedTemporaryFile(suffix='.mp3')
        shutil.copy(master_file, self.working_file.name)

    def _image_data(self, filename):
        return open(filename, 'rb').read()

    #todo we need to build different test data each test
    def _populate_tags(self, tags):
        test_mp3 = mp3.MP3(self.working_file.name)
        test_mp3.add_tags()
        test_mp3.tags.add(id3.TALB(encoding=3, text=tags['release_name']))
        test_mp3.tags.add(id3.APIC(3, tags['back_cover_picture'][0], 4, 'Back Cover',
                                   self._image_data(tags['back_cover_picture'][1])))
        test_mp3.tags.add(id3.APIC(3, tags['front_cover_picture'][0], 3, '',
                                   self._image_data(tags['front_cover_picture'][1])))
        test_mp3.tags.add(id3.TPE1(encoding=3, text=tags['lead_performer']))
        test_mp3.tags.add(id3.TDOR(encoding=3, text=[id3.ID3TimeStamp(tags[
            'original_release_date'])]))
        test_mp3.tags.add(id3.TIT2(encoding=3, text=tags['track_title']))
        test_mp3.tags.add(id3.TPE4(encoding=3, text=tags['version_info']))
        test_mp3.save()

    def _delete_test_mp3(self):
        self.working_file.close()