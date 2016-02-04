# -*- coding: utf-8 -*-

import os

from mutagen.flac import FLAC, Picture

from test.util import resources
from tgit import fs


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
            if tag == 'lead_performer' or tag == 'ARTIST':
                self._add_tag("ARTIST", value)
            elif tag == 'release_name' or tag == 'ALBUM':
                self._add_tag("ALBUM", value)
            elif tag == 'label_name' or tag == 'ORGANIZATION':
                self._add_tag("ORGANIZATION", value)
            elif tag == 'primary_style' or tag == 'GENRE':
                self._add_tag("GENRE", value)
            elif tag == 'recording_time' or tag == 'DATE':
                self._add_tag("DATE", value)
            elif tag == 'track_title' or tag == 'TITLE':
                self._add_tag("TITLE", value)
            elif tag == 'isrc' or tag == 'ISRC':
                self._add_tag("ISRC", value)
            elif tag == 'iswc' or tag == 'ISWC':
                self._add_tag("ISWC", value)
            elif tag == 'TAGGER':
                self._add_tag("TAGGER", value)
            elif tag == 'TAGGER_VERSION':
                self._add_tag("TAGGER-VERSION", value)
            elif tag == 'TAGGING_TIME':
                self._add_tag("TAGGING-TIME", value)
            elif tag == 'TRACKNUMBER':
                self._add_tag("TRACKNUMBER", value)
            elif tag == 'TRACKTOTAL':
                self._add_tag("TRACKTOTAL", value)
            elif tag == 'PICTURES':
                for mime, type_, desc, data in value:
                    self._add_picture(mime, type_, desc, data)
            elif tag == 'LEAD_PERFORMER_REGION':
                self._add_tag("LEAD-PERFORMER-REGION", value)
            elif tag == 'PRODUCER':
                self._add_tag("PRODUCER", value)
            elif tag == 'PRODUCER_REGION':
                self._add_tag("PRODUCER-REGION", value)
            elif tag == 'RECORDING_STUDIO':
                self._add_tag("RECORDING-STUDIO", value)
            elif tag == 'RECORDING_STUDIO_REGION':
                self._add_tag("RECORDING-STUDIO-REGION", value)
            elif tag == 'MUSIC_PRODUCER':
                self._add_tag("MUSIC-PRODUCER", value)
            elif tag == 'ISNI':
                self._add_tag("ISNI", value)
            elif tag == 'LYRICIST':
                self._add_tag("LYRICIST", value)
            elif tag == 'CATALOGNUMBER':
                self._add_tag("CATALOGNUMBER", value)
            elif tag == 'BARCODE':
                self._add_tag("BARCODE", value)
            elif tag == 'MIXER':
                self._add_tag("MIXER", value)
            elif tag == 'COMMENT':
                self._add_tag("COMMENT", value)
            elif tag == 'PUBLISHER':
                self._add_tag("PUBLISHER", value)
            elif tag == 'COMPOSER':
                self._add_tag("COMPOSER", value)
            elif tag == 'VERSION':
                self._add_tag("VERSION", value)
            elif tag == 'LYRICS':
                self._add_tag("LYRICS", value)
            elif tag == 'LANGUAGE':
                self._add_tag("LANGUAGE", value)
            elif tag == 'COMPILATION':
                self._add_tag("COMPILATION", value)
            elif tag == 'GUEST_ARTIST':
                self._add_tag("GUEST ARTIST", value)
            else:
                raise AssertionError("Unsupported tag '%s'" % tag)

    def _add_tag(self, key, value):
        self._flac.tags.append((key, value))

    def _add_picture(self, mime, type_, desc, data):
        picture = Picture()
        picture.data = data
        picture.mime = mime
        picture.type = type_
        picture.desc = desc
        self._flac.add_picture(picture)

    def _save(self):
        self._flac.save()
