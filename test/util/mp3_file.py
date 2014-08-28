# -*- coding: utf-8 -*-

import os

from mutagen import id3
from mutagen.mp3 import MP3

from test.util import resources as testResources

from tgit.util import fs


class Base(object):
    filename = testResources.path('base.mp3')
    bitrate = 320000
    duration = 9.064475

UTF_8 = 3
FRONT_COVER = 3
BACK_COVER = 4


def mp3File(from_=Base.filename, to=None):
    return Mp3File(fs.makeTempCopy(from_, to))


class Mp3File(object):
    def __init__(self, filename):
        self._filename = filename
        self._mp3 = self._load(filename)

    def _load(self, filename):
        mp3 = MP3(filename)
        if not mp3.tags:
            mp3.add_tags()
        return mp3

    @property
    def filename(self):
        return self._filename

    def delete(self):
        os.remove(self.filename)

    def withTags(self, **tags):
        self._writeTags(tags)
        return self

    def _writeTags(self, tags):
        for tag, value in tags.items():
            if tag == 'releaseName' or tag == 'TALB':
                self.addTag(id3.TALB(encoding=UTF_8, text=value))
            elif tag == 'frontCover' or tag == 'APIC_FRONT':
                mime, desc, data = value
                self.addTag(id3.APIC(UTF_8, mime, FRONT_COVER, desc, data))
            elif tag == 'backCover' or tag == 'APIC_BACK':
                mime, desc, data = value
                self.addTag(id3.APIC(UTF_8, mime, BACK_COVER, desc, data))
            elif tag == 'leadPerformer' or tag == 'TPE1':
                self.addTag(id3.TPE1(encoding=UTF_8, text=value))
            elif tag == 'guestPerformers' or tag == 'TMCL':
                self.addTag(id3.TMCL(encoding=UTF_8, people=value))
            elif tag == 'labelName' or tag == 'TOWN':
                self.addTag(id3.TOWN(encoding=UTF_8, text=value))
            elif tag == 'catalogNumber' or tag == 'TXXX_CATALOG_NUMBER':
                self.addTag(id3.TXXX(encoding=UTF_8, desc='Catalog Number', text=value))
            elif tag == 'upc' or tag == 'TXXX_UPC':
                self.addTag(id3.TXXX(encoding=UTF_8, desc='UPC', text=value))
            elif tag == 'recordingTime' or tag == 'TDRC':
                self.addTag(id3.TDRC(encoding=UTF_8, text=[id3.ID3TimeStamp(value)]))
            elif tag == 'releaseTime' or tag == 'TDRL':
                self.addTag(id3.TDRL(encoding=UTF_8, text=[id3.ID3TimeStamp(value)]))
            elif tag == 'originalReleaseTime' or tag == 'TDOR':
                self.addTag(id3.TDOR(encoding=UTF_8, text=[id3.ID3TimeStamp(value)]))
            elif tag == 'recordingStudios' or tag == 'TXXX_RECORDING_STUDIOS':
                self.addTag(id3.TXXX(encoding=UTF_8, desc='Recording Studios', text=value))
            elif tag == 'TIPL':
                self.addTag(id3.TIPL(encoding=UTF_8, people=value))
            elif tag == 'comments' or tag == 'COMM':
                text, lang = value
                self.addTag(id3.COMM(encoding=UTF_8, text=text, desc='', lang=lang))
            elif tag == 'trackTitle' or tag == 'TIT2':
                self.addTag(id3.TIT2(encoding=UTF_8, text=value))
            elif tag == 'versionInfo' or tag == 'TPE4':
                self.addTag(id3.TPE4(encoding=UTF_8, text=value))
            elif tag == 'featuredGuest' or tag == 'TXXX_FEATURED_GUEST':
                self.addTag(id3.TXXX(encoding=UTF_8, desc='Featured Guest', text=value))
            elif tag == 'lyricist' or tag == 'TEXT':
                self.addTag(id3.TEXT(encoding=UTF_8, text=value))
            elif tag == 'composer' or tag == 'TCOM':
                self.addTag(id3.TCOM(encoding=UTF_8, text=value))
            elif tag == 'publisher' or tag == 'TPUB':
                self.addTag(id3.TPUB(encoding=UTF_8, text=value))
            elif tag == 'isrc' or tag == 'TSRC':
                self.addTag(id3.TSRC(encoding=UTF_8, text=value))
            elif tag == 'labels' or tag == 'TXXX_TAGS':
                self.addTag(id3.TXXX(encoding=UTF_8, desc='Tags', text=value))
            elif tag == 'isni' or tag == 'TXXX_ISNI':
                self.addTag(id3.TXXX(encoding=UTF_8, desc='ISNI', text=value))
            elif tag == 'lyrics' or tag == 'USLT':
                text, lang = value
                self.addTag(id3.USLT(encoding=UTF_8, text=text, desc='', lang=lang))
            elif tag == 'language' or tag == 'TLAN':
                self.addTag(id3.TLAN(encoding=UTF_8, text=value))
            elif tag == 'primaryStyle' or tag == 'TCON':
                self.addTag(id3.TCON(encoding=UTF_8, text=value))
            elif tag == 'compilation' or tag == 'TCMP':
                self.addTag(id3.TCMP(encoding=UTF_8, text=value))
            elif tag == 'tagger' or tag == 'TXXX_TAGGER':
                self.addTag(id3.TXXX(encoding=UTF_8, desc='Tagger', text=value))
            elif tag == 'taggingTime' or tag == 'TXXX_TAGGING_TIME':
                self.addTag(id3.TXXX(encoding=UTF_8, desc='Tagging Time', text=value))
            else:
                raise AssertionError("Knows nothing about '%s'" % tag)

    def addTag(self, tag):
        self._mp3.tags.add(tag)

    def make(self):
        self._mp3.save()
        return self

