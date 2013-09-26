# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
import mutagen.mp3 as mp3
import mutagen.id3 as id3

import resources


class Sample(object):
    pass


mp3Sample = Sample()
mp3Sample.path = resources.path("base.mp3")
mp3Sample.bitrate = 320000
mp3Sample.duration = 9.064475
mp3Sample.durationAsText = "00:09"


# todo move to a file related utilities module
def readContent(filename):
    return open(filename, "rb").read()


# todo move to a file related utilities module
def makeCopy(originalFile):
    workingFile, path = tempfile.mkstemp(suffix='.mp3')
    try:
        shutil.copy(originalFile, path)
    finally:
        os.close(workingFile)
    return path


def MP3(master, **tags):
    return MP3Builder(makeCopy(master)).withTags(**tags)


UTF_8 = 3


class MP3Builder(object):
    def __init__(self, path):
        self._file = path
        self._mp3 = mp3.MP3(self._file)
        if not self._mp3.tags:
            self._mp3.add_tags()

    @property
    def name(self):
        return self._file

    def delete(self):
        os.remove(self.name)

    def withTags(self, **tags):
        self._writeTags(tags)
        return self

    def _writeTags(self, tags):
        if 'releaseName' in tags:
            self._mp3.tags.add(id3.TALB(encoding=UTF_8, text=tags['releaseName']))
        if 'frontCover' in tags:
            self._attachPicture(3, *tags['frontCover'])
        if 'backCover' in tags:
            self._attachPicture(4, *tags['backCover'])
        if 'leadPerformer' in tags:
            self._mp3.tags.add(id3.TPE1(encoding=UTF_8, text=tags['leadPerformer']))
        if 'releaseDate' in tags:
            self._mp3.tags.add(id3.TDRL(encoding=UTF_8, text=[id3.ID3TimeStamp(tags[
                'releaseDate'])]))
        if 'upc' in tags:
            self._mp3.tags.add(id3.TXXX(encoding=UTF_8, desc='UPC', text=tags['upc']))
        if 'trackTitle' in tags:
            self._mp3.tags.add(id3.TIT2(encoding=UTF_8, text=tags['trackTitle']))
        if 'versionInfo' in tags:
            self._mp3.tags.add(id3.TPE4(encoding=UTF_8, text=tags['versionInfo']))
        if 'featuredGuest' in tags:
            self._mp3.tags.add(id3.TXXX(encoding=UTF_8, desc='Featured Guest',
                                        text=tags['featuredGuest']))
        if 'isrc' in tags:
            self._mp3.tags.add(id3.TSRC(encoding=UTF_8, text=tags['isrc']))

        self._mp3.save()

    def _attachPicture(self, type_, mime, desc, data):
        self._mp3.tags.add(id3.APIC(UTF_8, mime, type_, desc, readContent(data)))

