# -*- coding: utf-8 -*-
import shutil

from hamcrest import *
import pytest

from test.util import mp3_file, flac_file
from tgit.tagging import embedded_metadata


@pytest.yield_fixture
def mp3(tmpdir):
    def maker(**tags):
        return mp3_file.make(to=tmpdir.strpath, **tags).filename

    yield maker
    shutil.rmtree(tmpdir.strpath)


@pytest.yield_fixture
def flac(tmpdir):
    def maker(**tags):
        return flac_file.make(to=tmpdir.strpath, **tags).filename

    yield maker
    shutil.rmtree(tmpdir.strpath)


def test_selects_mp3_container_to_handle_mp3_files(mp3):
    metadata = embedded_metadata.load(mp3(release_name="Honeycomb"))
    assert_that(metadata, has_entry('releaseName', not_none()), 'embedded metadata')


def test_selects_flac_container_to_handle_flac_files(flac):
    metadata = embedded_metadata.load(flac(lead_performer="Joel Miller"))
    assert_that(metadata, has_entry('leadPerformer', not_none()), 'embbeded metadata')


def test_returns_empty_metadata_in_case_of_unsupported_format():
    metadata = embedded_metadata.load('audio.???')
    assert_that(metadata, empty(), 'embedded metadata')