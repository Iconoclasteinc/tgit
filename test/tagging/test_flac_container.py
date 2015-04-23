# -*- coding: utf-8 -*-

import shutil

from hamcrest import assert_that, has_entry, has_items, has_length
import pytest

from test.util import flac_file
from tgit.tagging.flac_container import FlacContainer
from tgit.metadata import Metadata

DURATION = flac_file.base.duration
BITRATE = flac_file.base.bitrate

container = FlacContainer()


@pytest.yield_fixture
def flac(tmpdir):
    def maker(**tags):
        return flac_file.make(to=tmpdir.strpath, **tags).filename

    yield maker
    shutil.rmtree(tmpdir.strpath)


def test_reads_lead_performer_from_artists_field(flac):
    metadata = container.load(flac(ARTIST="Joel Miller"))
    assert_that(metadata, has_entry('lead_performer', "Joel Miller"), "metadata")


def test_reads_bitrate_from_audio_stream_information(flac):
    metadata = container.load(flac())
    assert_that(metadata, has_entry('bitrate', BITRATE), "bitrate")


def test_reads_duration_from_audio_stream_information(flac):
    metadata = container.load(flac())
    assert_that(metadata, has_entry('duration', DURATION), "duration")


def test_reads_track_title_from_title_field(flac):
    metadata = container.load(flac(TITLE="Salsa Coltrane"))
    assert_that(metadata, has_entry('track_title', "Salsa Coltrane"), "metadata")


def test_reads_release_name_from_album_field(flac):
    metadata = container.load(flac(ALBUM="Honeycomb"))
    assert_that(metadata, has_entry('release_name', "Honeycomb"), "metadata")


def test_reads_primary_style_from_genre_field(flac):
    metadata = container.load(flac(GENRE="Modern Jazz"))
    assert_that(metadata, has_entry('primary_style', "Modern Jazz"), "metadata")


def test_reads_track_i_s_r_c_from_i_s_r_c_field(flac):
    metadata = container.load(flac(ISRC="CABL31201254"))
    assert_that(metadata, has_entry('isrc', "CABL31201254"), "metadata")


def test_reads_recording_time_from_date_field(flac):
    metadata = container.load(flac(DATE="2011-11-02"))
    assert_that(metadata, has_entry('recording_time', "2011-11-02"), "metadata")


def test_reads_label_name_from_organization_field(flac):
    metadata = container.load(flac(ORGANIZATION="Effendi Records Inc."))
    assert_that(metadata, has_entry('label_name', "Effendi Records Inc."), "metadata")


def test_round_trips_metadata_to_file(flac):
    metadata = Metadata()
    metadata['release_name'] = "St-Henri"
    metadata['lead_performer'] = "Joel Miller"
    metadata['label_name'] = "Effendi Records Inc."
    metadata['primary_style'] = "Modern Jazz"
    metadata['recording_time'] = "2007-11-02"
    metadata['track_title'] = "Salsa Coltrane"
    metadata['isrc'] = "CABL31201254"

    assert_can_be_saved_and_reloaded_with_same_state(flac, metadata)


def test_removes_comment_field_when_tag_not_in_metadata(flac):
    filename = flac(ARTIST="Joel Miller")
    container.save(filename, Metadata())
    assert_contains_metadata(filename, Metadata())


def assert_can_be_saved_and_reloaded_with_same_state(flac, metadata):
    filename = flac()
    container.save(filename, metadata.copy())
    assert_contains_metadata(filename, metadata)


def assert_contains_metadata(filename, expected):
    expected_length = len(expected) + len(('bitrate', 'duration'))
    metadata = container.load(filename)
    assert_that(list(metadata.items()), has_items(*list(expected.items())), "metadata items")
    assert_that(metadata, has_length(expected_length), "metadata count")