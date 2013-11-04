# -*- coding: utf-8 -*-

import os

from mutagen import id3, mp3

from test.util import resources as testResources

from tgit import tags as tagging, fs


class TestMp3(object):
    filename = testResources.path('base.mp3')
    bitrate = 320000
    duration = 9.064475

UTF_8 = 3
FRONT_COVER = 3
BACK_COVER = 4


def makeMp3(from_=TestMp3.filename, **tags):
    return Mp3(fs.makeCopy(from_)).withTags(**tags).make()


class Mp3(object):
    def __init__(self, filename):
        self._filename = filename
        self._tags = self._loadTags(filename)

    def _loadTags(self, filename):
        self._mp3 = mp3.MP3(filename)
        if not self._mp3.tags:
            self._mp3.add_tags()
        return self._mp3.tags

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
            if tag == tagging.RELEASE_NAME or tag == 'TALB':
                self._tags.add(id3.TALB(encoding=UTF_8, text=value))
            elif tag == 'frontCover' or tag == 'APIC_FRONT':
                mime, desc, data = value
                self._tags.add(id3.APIC(UTF_8, mime, FRONT_COVER, desc, data))
            elif tag == 'backCover' or tag == 'APIC_BACK':
                mime, desc, data = value
                self._tags.add(id3.APIC(UTF_8, mime, BACK_COVER, desc, data))
            elif tag == tagging.LEAD_PERFORMER or tag == 'TPE1':
                self._tags.add(id3.TPE1(encoding=UTF_8, text=value))
            elif tag == tagging.GUEST_PERFORMERS or tag == 'TPE2':
                self._tags.add(id3.TPE2(encoding=UTF_8, text=value))
            elif tag == tagging.LABEL_NAME or tag == 'TOWN':
                self._tags.add(id3.TOWN(encoding=UTF_8, text=value))
            elif tag == tagging.CATALOG_NUMBER or tag == 'TXXX_CATALOG_NUMBER':
                self._tags.add(id3.TXXX(encoding=UTF_8, desc='Catalog Number', text=value))
            elif tag == tagging.UPC or tag == 'TXXX_UPC':
                self._tags.add(id3.TXXX(encoding=UTF_8, desc='UPC', text=value))
            elif tag == tagging.RECORDING_TIME or tag == 'TDRC':
                self._tags.add(id3.TDRC(encoding=UTF_8, text=[id3.ID3TimeStamp(value)]))
            elif tag == tagging.RELEASE_TIME or tag == 'TDRL':
                self._tags.add(id3.TDRL(encoding=UTF_8, text=[id3.ID3TimeStamp(value)]))
            elif tag == tagging.ORIGINAL_RELEASE_TIME or tag == 'TDOR':
                self._tags.add(id3.TDOR(encoding=UTF_8, text=[id3.ID3TimeStamp(value)]))
            elif tag == tagging.RECORDING_STUDIOS or tag == 'TXXX_RECORDING_STUDIOS':
                self._tags.add(id3.TXXX(encoding=UTF_8, desc='Recording Studios', text=value))
            elif tag == tagging.TRACK_TITLE or tag == 'TIT2':
                self._tags.add(id3.TIT2(encoding=UTF_8, text=value))
            elif tag == tagging.VERSION_INFO or tag == 'TPE4':
                self._tags.add(id3.TPE4(encoding=UTF_8, text=value))
            elif tag == tagging.FEATURED_GUEST or tag == 'TXXX_FEATURED_GUEST':
                self._tags.add(id3.TXXX(encoding=UTF_8, desc='Featured Guest', text=value))
            elif tag == tagging.ISRC or tag == 'TSRC':
                self._tags.add(id3.TSRC(encoding=UTF_8, text=value))
            else:
                raise AssertionError("Knows nothing about '%s'" % tag)

    def make(self):
        self._mp3.save()
        return self._mp3

