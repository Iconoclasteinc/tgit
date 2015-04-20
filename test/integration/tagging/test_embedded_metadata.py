# -*- coding: utf-8 -*-
from hamcrest import *
import pytest

from tgit.tagging import embedded_metadata
from test.util import mp3_file as mp3


@pytest.fixture
def mp3_file(request):
    audio = mp3.make(releaseName="Honeycomb")
    request.addfinalizer(audio.delete)
    return audio.filename


def test_selects_mp3_container_when_handling_mp3_files(mp3_file):
    metadata = embedded_metadata.load(mp3_file)
    assert_that(metadata, has_entry('releaseName', not_none()), 'metadata')