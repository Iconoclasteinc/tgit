# -*- coding: utf-8 -*-

import os

from mutagen import id3
from mutagen.mp3 import MP3

from test.util import resources as test_resources
from tgit import fs


class Base(object):
    filename = test_resources.path("base.mp3")
    bitrate = 320000
    duration = 9.064475


def make(from_=Base.filename, to=None, **tags):
    audio = Mp3Audio(fs.make_temp_copy(from_, to))
    audio.tag(**tags)
    return audio


UTF_8 = 3
FRONT_COVER = 3
BACK_COVER = 4


class Mp3Audio(object):
    def __init__(self, filename):
        self.filename = filename
        self._mp3 = self._load(filename)

    @staticmethod
    def _load(filename):
        audio = MP3(filename)
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
            if tag == "releaseName" or tag == "release_name" or tag == "TALB":
                self._add_tag(id3.TALB(encoding=UTF_8, text=value))
            elif tag == "front_cover" or tag == "APIC_FRONT":
                mime, desc, data = value
                self._add_tag(id3.APIC(UTF_8, mime, FRONT_COVER, desc, data))
            elif tag == "backCover" or tag == "APIC_BACK":
                mime, desc, data = value
                self._add_tag(id3.APIC(UTF_8, mime, BACK_COVER, desc, data))
            elif tag == "lead_performer" or tag == "TPE1":
                self._add_tag(id3.TPE1(encoding=UTF_8, text=value))
            elif tag == "lead_performer_region" or tag == "TXXX_LEAD_PERFORMER_REGION":
                self._add_tag(id3.TXXX(encoding=UTF_8, desc="LEAD-PERFORMER-REGION", text=value))
            elif tag == "guestPerformers" or tag == "TMCL":
                self._add_tag(id3.TMCL(encoding=UTF_8, people=value))
            elif tag == "label_name" or tag == "TOWN":
                self._add_tag(id3.TOWN(encoding=UTF_8, text=value))
            elif tag == "catalogNumber" or tag == "TXXX_CATALOG_NUMBER":
                self._add_tag(id3.TXXX(encoding=UTF_8, desc="Catalog Number", text=value))
            elif tag == "upc" or tag == "TXXX_UPC":
                """ Deprecated and replaced with BARCODE """
                self._add_tag(id3.TXXX(encoding=UTF_8, desc="UPC", text=value))
            elif tag == "barcode" or tag == "TXXX_BARCODE":
                self._add_tag(id3.TXXX(encoding=UTF_8, desc="BARCODE", text=value))
            elif tag == "recording_time" or tag == "TDRC":
                self._add_tag(id3.TDRC(encoding=UTF_8, text=[id3.ID3TimeStamp(value)]))
            elif tag == "releaseTime" or tag == "TDRL":
                self._add_tag(id3.TDRL(encoding=UTF_8, text=[id3.ID3TimeStamp(value)]))
            elif tag == "originalReleaseTime" or tag == "TDOR":
                self._add_tag(id3.TDOR(encoding=UTF_8, text=[id3.ID3TimeStamp(value)]))
            elif tag == "tagging_time" or tag == "TDTG":
                self._add_tag(id3.TDTG(encoding=UTF_8, text=[id3.ID3TimeStamp(value)]))
            elif tag == "recordingStudios" or tag == "TXXX_RECORDING_STUDIO":
                self._add_tag(id3.TXXX(encoding=UTF_8, desc="Recording Studio", text=value))
            elif tag == "TIPL":
                self._add_tag(id3.TIPL(encoding=UTF_8, people=value))
            elif tag == "comments" or tag == "COMM":
                text, lang = value
                self._add_tag(id3.COMM(encoding=UTF_8, text=text, desc="", lang=lang))
            elif tag == "track_title" or tag == "TIT2":
                self._add_tag(id3.TIT2(encoding=UTF_8, text=value))
            elif tag == "version_info" or tag == "TPE4":
                self._add_tag(id3.TPE4(encoding=UTF_8, text=value))
            elif tag == "featured_guest" or tag == "TXXX_FEATURED_GUEST":
                self._add_tag(id3.TXXX(encoding=UTF_8, desc="Featured Guest", text=value))
            elif tag == "lyricist" or tag == "TEXT":
                self._add_tag(id3.TEXT(encoding=UTF_8, text=value))
            elif tag == "composer" or tag == "TCOM":
                self._add_tag(id3.TCOM(encoding=UTF_8, text=value))
            elif tag == "publisher" or tag == "TPUB":
                self._add_tag(id3.TPUB(encoding=UTF_8, text=value))
            elif tag == "isrc" or tag == "TSRC":
                self._add_tag(id3.TSRC(encoding=UTF_8, text=value))
            elif tag == "labels" or tag == "TXXX_TAGS":
                self._add_tag(id3.TXXX(encoding=UTF_8, desc="Tags", text=value))
            elif tag == "isni" or tag == "TXXX_ISNI_Joel_Miller":
                self._add_tag(id3.TXXX(encoding=UTF_8, desc="ISNI:Joel Miller", text=value))
            elif tag == "TXXX_ISNI_Rebecca_Ann_Maloy":
                self._add_tag(id3.TXXX(encoding=UTF_8, desc="ISNI:Rebecca Ann Maloy", text=value))
            elif tag == "TXXX_ISNI":
                self._add_tag(id3.TXXX(encoding=UTF_8, desc="ISNI", text=value))
            elif tag == "iswc" or tag == "TXXX_ISWC":
                self._add_tag(id3.TXXX(encoding=UTF_8, desc="ISWC", text=value))
            elif tag == "lyrics" or tag == "USLT":
                text, lang = value
                self._add_tag(id3.USLT(encoding=UTF_8, text=text, desc="", lang=lang))
            elif tag == "language" or tag == "TLAN":
                self._add_tag(id3.TLAN(encoding=UTF_8, text=value))
            elif tag == "primary_style" or tag == "TCON":
                self._add_tag(id3.TCON(encoding=UTF_8, text=value))
            elif tag == "compilation" or tag == "TCMP":
                self._add_tag(id3.TCMP(encoding=UTF_8, text=value))
            elif tag == "tagger" or tag == "TXXX_TAGGER":
                self._add_tag(id3.TXXX(encoding=UTF_8, desc="TAGGER", text=value))
            elif tag == "TXXX_Tagger":
                """ Deprecated and replaced with separate TAGGER and VERSION tags """
                self._add_tag(id3.TXXX(encoding=UTF_8, desc="Tagger", text=value))
            elif tag == "tagger_version" or tag == "TXXX_TAGGER_VERSION":
                self._add_tag(id3.TXXX(encoding=UTF_8, desc="TAGGER_VERSION", text=value))
            elif tag == "TXXX_Tagging_Time":
                """ Deprecated and replaced with TAGGING_TIME """
                self._add_tag(id3.TXXX(encoding=UTF_8, desc="Tagging Time", text=value))
            elif tag == "TXXX_TAGGING_TIME":
                """ Deprecated and replaced with TDTG """
                self._add_tag(id3.TXXX(encoding=UTF_8, desc="TAGGING_TIME", text=value))
            elif tag == "TXXX_PRODUCTION_COMPANY":
                self._add_tag(id3.TXXX(encoding=UTF_8, desc="PRODUCTION-COMPANY", text=value))
            elif tag == "TXXX_PRODUCTION_COMPANY_REGION":
                self._add_tag(id3.TXXX(encoding=UTF_8, desc="PRODUCTION-COMPANY-REGION", text=value))
            elif tag == "TXXX_RECORDING_STUDIO_REGION":
                self._add_tag(id3.TXXX(encoding=UTF_8, desc="RECORDING-STUDIO-REGION", text=value))
            elif tag == "TRCK":
                self._add_tag(id3.TRCK(encoding=UTF_8, text=value))
            else:
                raise AssertionError("Knows nothing about '{0}'".format(tag))

    def _add_tag(self, tag):
        self._mp3.tags.add(tag)

    def _save(self):
        self._mp3.save()
