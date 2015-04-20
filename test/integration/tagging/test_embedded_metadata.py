# -*- coding: utf-8 -*-
from hamcrest import *
import pytest

from tgit.tagging import embedded_metadata
from test.util import mp3_file as mp3, flac_file as flac


@pytest.yield_fixture
def mp3_file():
    audio = mp3.make(releaseName="Honeycomb")
    yield audio.filename
    audio.delete()


@pytest.yield_fixture
def flac_file():
    audio = flac.make(lead_performer="Joel Miller")
    yield audio.filename
    audio.delete()


def test_selects_mp3_container_to_handle_mp3_files(mp3_file):
    metadata = embedded_metadata.load(mp3_file)
    assert_that(metadata, has_entry('releaseName', not_none()), 'embedded metadata')


def test_selects_flac_container_to_handle_flac_files(flac_file):
    metadata = embedded_metadata.load(flac_file)
    assert_that(metadata, has_entry('leadPerformer', not_none()), 'embbeded metadata')


def test_returns_empty_metadata_in_case_of_unsupported_format():
    metadata = embedded_metadata.load('audio.???')
    assert_that(metadata, empty(), 'embedded metadata')