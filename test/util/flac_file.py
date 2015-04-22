# -*- coding: utf-8 -*-

import os
from mutagen.flac import FLAC

from test.util import resources
from tgit.util import fs


class base(object):
    filename = resources.path('base.flac')
    bitrate = 705600
    duration = 5.0


def make(from_=base.filename, to=None, **tags):
    audio = FlacAudio(fs.make_temp_copy(from_, to))
    audio.tag(**tags)
    return audio


class FlacAudio(object):
    def __init__(self, filename):
        self.filename = filename
        self._flac = self._load(filename)

    @staticmethod
    def _load(filename):
        audio = FLAC(filename)
        if audio.tags is None:
            audio.add_tags()
        return audio

    def delete(self):
        os.remove(self.filename)

    def tag(self, **tags):
        self._write_tags(tags)
        self._save()

    def _write_tags(self, tags):
        for tag, value in tags.items():
            if tag == 'lead_performer':
                self._add_tag("ARTIST", value)
            elif tag == 'release_name':
                self._add_tag("ALBUM", value)
            elif tag == 'track_title':
                self._add_tag("TITLE", value)
            else:
                raise AssertionError("Unsupported tag '%s'" % tag)

    def _add_tag(self, key, value):
        self._flac.tags.append((key, value))

    def _save(self):
        self._flac.save()