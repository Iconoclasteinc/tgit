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


def test_reads_lead_performer_from_vorbis_comments(flac):
    metadata = container.load(flac(lead_performer='Lead Artist'))
    assert_that(metadata, has_entry('leadPerformer', 'Lead Artist'), 'metadata')


def test_reads_bitrate_from_audio_stream_information(flac):
    metadata = container.load(flac())
    assert_that(metadata, has_entry('bitrate', BITRATE), 'bitrate')


def test_reads_duration_from_audio_stream_information(flac):
    metadata = container.load(flac())
    assert_that(metadata, has_entry('duration', DURATION), 'duration')


def test_round_trips_metadata_to_file(flac):
    metadata = Metadata()
    metadata['leadPerformer'] = 'Lead Performer'

    assert_can_be_saved_and_reloaded_with_same_state(flac, metadata)


# test that we handle metadata without value gracefully on load
# test that metadata value overrides existing comment fields
# test that an empty metadata value does not produce a comment field


def assert_can_be_saved_and_reloaded_with_same_state(flac, metadata):
    filename = flac()
    container.save(filename, metadata.copy())
    assert_contains_metadata(filename, metadata)


def assert_contains_metadata(filename, expected):
    expected_length = len(expected) + len(('bitrate', 'duration'))
    metadata = container.load(filename)
    assert_that(list(metadata.items()), has_items(*list(expected.items())), 'metadata items')
    assert_that(metadata, has_length(expected_length), 'metadata count')