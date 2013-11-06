# -*- coding: utf-8 -*-
#
# TGiT, Music Tagger for Professionals
# Copyright (C) 2013 Iconoclaste Musique Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

from collections import defaultdict

from mutagen import mp3, id3

from tgit import tags as tagging
from tgit.metadata import Metadata, Image


def invert(mapping):
    return dict([(v, k) for k, v in mapping.iteritems()])


class NoMpegInfo(object):
    bitrate = 0
    length = 0


def load(filename):
    mp3 = MP3File(filename)
    mp3.load()
    return mp3


def save(filename, metadata):
    mp3 = MP3File(filename)
    mp3.save(metadata)
    return mp3


class MP3File(object):
    UTF_8 = 3

    class TextRecords(object):
        def __init__(self, mapping):
            self._mapping = mapping

        def collectMetadata(self, metadata, frames):
            for frameKey, tag in self._mapping.items():
                if frameKey in frames:
                    metadata[tag] = unicode(frames[frameKey])

        def collectFrames(self, frames, encoding, metadata):
            for frameKey, tag in self._mapping.items():
                if tag in metadata:
                    id, desc, = self._decompose(frameKey)
                    frames.add(getattr(id3, id)(encoding=encoding, desc=desc, text=metadata[tag]))

        def _decompose(self, key):
            if ':' in key:
                return key.split(':')
            else:
                return key, None

    class ImageRecords(object):
        def __init__(self, frameId, pictureTypes):
            self._frameId = frameId
            self._pictureTypes = pictureTypes

        def collectMetadata(self, metadata, frames):
            for picture in self._pictureFrames(frames):
                imageType = self._pictureTypes.get(picture.type, Image.OTHER)
                metadata.addImage(picture.mime, picture.data, imageType, picture.desc)

        def _pictureFrames(self, frames):
            return [frame for key, frame in frames.items() if key.startswith(self._frameId)]

        def collectFrames(self, frames, encoding, metadata):
            frames.delall(self._frameId)
            count = defaultdict(lambda: 0)

            for image in metadata.images:
                frames.add(self._makePictureFrame(count, encoding, image))

        def _makePictureFrame(self, count, encoding, image):
            description = image.desc
            if count[image.desc] > 0:
                description += " (%i)" % (count[image.desc] + 1)
            count[image.desc] += 1
            imagesTypes = invert(self._pictureTypes)
            return getattr(id3, self._frameId)(encoding=encoding, mime=image.mime,
                                               type=imagesTypes[image.type],
                                               desc=description, data=image.data)

    class PeopleRecords(object):
        def __init__(self, mapping):
            self._mapping = mapping

        def collectMetadata(self, metadata, frames):
            for frameKey, tag in self._mapping.items():
                if frameKey in frames:
                    metadata[tag] = []
                    for role, name in frames[frameKey].people:
                        metadata[tag].append((role, name))

        def collectFrames(self, frames, encoding, metadata):
            for frameKey, tag in self._mapping.items():
                if tag in metadata:
                    frame = getattr(id3, frameKey)(encoding=encoding)
                    for role, name in metadata[tag]:
                        frame.people.append([role, name])
                    frames.add(frame)

    __TEXT_FRAMES = {'TALB': tagging.RELEASE_NAME,
                     'TPE1': tagging.LEAD_PERFORMER,
                     'TOWN': tagging.LABEL_NAME,
                     'TDRC': tagging.RECORDING_TIME,
                     'TDRL': tagging.RELEASE_TIME,
                     'TDOR': tagging.ORIGINAL_RELEASE_TIME,
                     'TIT2': tagging.TRACK_TITLE,
                     'TPE4': tagging.VERSION_INFO,
                     'TSRC': tagging.ISRC,
                     'TXXX:Catalog Number': tagging.CATALOG_NUMBER,
                     'TXXX:UPC': tagging.UPC,
                     'TXXX:Recording Studios': tagging.RECORDING_STUDIOS,
                     'TXXX:Featured Guest': tagging.FEATURED_GUEST, }

    __PICTURES_FRAMES = 'APIC'

    __PICTURES_TYPES = {
        0: Image.OTHER,
        3: Image.FRONT_COVER,
        4: Image.BACK_COVER,
    }

    __MUSICIANS_FRAMES = {
        'TMCL': tagging.GUEST_PERFORMERS
    }

    __RECORDS = [
        TextRecords(__TEXT_FRAMES),
        ImageRecords(__PICTURES_FRAMES, __PICTURES_TYPES),
        PeopleRecords(__MUSICIANS_FRAMES)
    ]

    def __init__(self, filename):
        super(MP3File, self).__init__()
        self._filename = filename
        self._metadata = Metadata()

    @property
    def filename(self):
        return self._filename

    def play(self, player):
        player.playMp3(self)

    @property
    def metadata(self):
        return self._metadata

    def load(self):
        audioFile = mp3.MP3(self._filename)

        frames = audioFile.tags or {}

        for record in self.__RECORDS:
            record.collectMetadata(self._metadata, frames)

        self._metadata[tagging.DURATION] = audioFile.info.length
        self._metadata[tagging.BITRATE] = audioFile.info.bitrate

        return self._metadata

    def save(self, metadata=None, encoding=UTF_8, overwrite=False, filename=None):
        if filename is None:
            filename = self._filename
        if metadata is None:
            metadata = self._metadata

        frames = self._loadFrames(filename)
        if overwrite:
            frames.clear()

        for record in self.__RECORDS:
            record.collectFrames(frames, encoding, metadata)

        frames.save(filename)

    def _loadFrames(self, filename):
        try:
            return id3.ID3(filename)
        except id3.ID3NoHeaderError:
            return id3.ID3()