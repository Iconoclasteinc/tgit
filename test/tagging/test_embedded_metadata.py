# -*- coding: utf-8 -*-
import shutil

from hamcrest import *
import pytest

from test.util import mp3_file, flac_file
from tgit.metadata import Metadata
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


def test_handles_mp3_files_using_mp3_container(mp3):
    audio = mp3()
    metadata = Metadata(leadPerformer="Joel Miller")
    embedded_metadata.save_metadata(audio, metadata)

    metadata = embedded_metadata.load_metadata(audio)
    assert_that(metadata, has_entry('leadPerformer', "Joel Miller"), 'embedded metadata')


def test_handles_flac_files_using_flac_container(flac):
    audio = flac()
    metadata = Metadata(leadPerformer="Joel Miller")
    embedded_metadata.save_metadata(audio, metadata)

    metadata = embedded_metadata.load_metadata(audio)
    assert_that(metadata, has_entry('leadPerformer', "Joel Miller"), 'embedded metadata')


def test_yields_empty_metadata_in_case_of_unsupported_format():
    metadata = embedded_metadata.load_metadata('audio.???')
    assert_that(metadata, empty(), 'embedded metadata')