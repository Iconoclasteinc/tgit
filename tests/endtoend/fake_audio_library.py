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

    def has_file_with_metadata(self, name, **tags):
        try:
            audio_file = MP3File(name)
        except IOError:
            raise AssertionError("Audio library contains no file " + name)

        assert_that(audio_file.release_name, equal_to(tags['release_name']),
                    "audio file release name")
        assert_that(audio_file.lead_performer, equal_to(tags['lead_performer']),
                    "audio file lead performer")
        assert_that(audio_file.track_title, equal_to(tags['track_title']),
                    "audio file track title")
        assert_that(audio_file.version_info, equal_to(tags['version_info']),
                    "audio file version information")

    def add_file(self, filename):
        imported_file = NamedTemporaryFile(suffix='.mp3')
        self._files.append(imported_file)
        shutil.copy(filename, imported_file.name)
        return imported_file.name