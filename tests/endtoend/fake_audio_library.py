# -*- coding: utf-8 -*-

import shutil
from tempfile import NamedTemporaryFile

from hamcrest.core.assert_that import assert_that
from hamcrest.core.core.isequal import equal_to

from tgit.mp3 import MP3File


# This is very rudimentary as of now
class FakeAudioLibrary(object):
    def __init__(self):
        self._files = []

    def destroy(self):
        [f.close() for f in self._files]

    def has_file_with_metadata(self, name, album, artist, title):
        try:
            audio_file = MP3File(name)
        except IOError:
            raise AssertionError("Audio library contains no file " + name)

        assert_that(audio_file.album_title, equal_to(album), "audio file album title")
        assert_that(audio_file.track_title, equal_to(title), "audio file track title")

    def add_file(self, filename):
        imported_file = NamedTemporaryFile(suffix='.mp3')
        self._files.append(imported_file)
        shutil.copy(filename, imported_file.name)
        return imported_file.name