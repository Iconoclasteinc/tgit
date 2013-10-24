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

import functools
from collections import defaultdict

from mutagen import mp3, id3

from tgit import album, track
from tgit.metadata import Metadata, Image

CUSTOM_FRAME_PREFIX = 'TXXX:'
UTF_8 = 3


def invert(mapping):
    return dict([(v, k) for k, v in mapping.iteritems()])


class NoMpegInfo(object):
    bitrate = 0
    length = 0


def load(filename):
    mp3 = MP3File(filename)
    mp3.load()
    return mp3


class MP3File(object):
    __ID3_TEXT_FRAMES = {
        'TALB': album.TITLE,
        'TPE1': album.LEAD_PERFORMER,
        'TPE2': album.GUEST_PERFORMERS,
        'TPUB': album.LABEL_NAME,
        'TDRC': album.RECORDING_TIME,
        'TDRL': album.RELEASE_TIME,
        'TDOR': album.ORIGINAL_RELEASE_TIME,
        'TXXX:UPC': album.UPC,
        'TIT2': track.TITLE,
        'TPE4': track.VERSION_INFO,
        'TXXX:Featured Guest': track.FEATURED_GUEST,
        'TSRC': track.ISRC
    }

    __METADATA_TAGS = invert(__ID3_TEXT_FRAMES)

    __PICTURES_FRAMES = ['APIC']

    __ID3_PICTURE_TYPES = {
        0: Image.OTHER,
        3: Image.FRONT_COVER,
        4: Image.BACK_COVER,
    }

    __METADATA_IMAGE_TYPES = invert(__ID3_PICTURE_TYPES)

    def __init__(self, filename):
        super(MP3File, self).__init__()
        self._filename = filename
        self._metadata = Metadata()
        self._mpegInfo = NoMpegInfo()

    # todo should we put filename, bitrate and duration in metadata?
    @property
    def filename(self):
        return self._filename

    @property
    def bitrate(self):
        return self._mpegInfo.bitrate

    @property
    def duration(self):
        return self._mpegInfo.length

    def metadata(self):
        return self._metadata.copy()

    def load(self):
        audioFile = mp3.MP3(self._filename)
        self._metadata = Metadata()
        self._mpegInfo = audioFile.info

        tags = audioFile.tags or {}
        for frame in tags.values():
            if self._isTextFrame(frame):
                self._addTextToMetadata(frame)
            elif self._isAttachedPicture(frame):
                self._addImageToMetadata(frame)

    def _isTextFrame(self, frame):
        return frame.HashKey in self.__ID3_TEXT_FRAMES

    def _addTextToMetadata(self, frame):
        tag = self.__ID3_TEXT_FRAMES[frame.HashKey]
        self._metadata[tag] = unicode(frame)

    def _isAttachedPicture(self, frame):
        return frame.FrameID in self.__PICTURES_FRAMES

    def _addImageToMetadata(self, frame):
        imageType = self.__ID3_PICTURE_TYPES.get(frame.type, Image.OTHER)
        self._metadata.addImage(frame.mime, frame.data, imageType, frame.desc)

    def save(self, metadata, encoding=UTF_8):
        tags = self._loadFramesOf(self._filename)

        for tag, value in metadata.items():
            tags.add(self._newTextFrame(encoding, tag, value))

        self._deleteAttachedPictures(tags)
        counters = defaultdict(lambda: 0)
        for image in metadata.images:
            tags.add(self._newPictureFrame(counters, image))

        tags.save(self._filename)

    def _loadFramesOf(self, filename):
        try:
            return id3.ID3(filename)
        except id3.ID3NoHeaderError:
            return id3.ID3()

    def _newTextFrame(self, encoding, tag, value):
        return self._convertTagToID3Frame(tag)(encoding=encoding, text=value)

    def _convertTagToID3Frame(self, meta):
        frameKey = self.__METADATA_TAGS[meta]
        if frameKey.startswith(CUSTOM_FRAME_PREFIX):
            return self._toCustomFrame(frameKey)
        else:
            return self._toTextFrame(frameKey)

    def _toCustomFrame(self, frameKey):
        return functools.partial(id3.TXXX, desc=frameKey[len(CUSTOM_FRAME_PREFIX):])

    def _toTextFrame(self, frameKey):
        return getattr(id3, frameKey)

    def _deleteAttachedPictures(self, tags):
        for frame in self.__PICTURES_FRAMES:
            tags.delall(frame)

    def _newPictureFrame(self, count, image):
        description = image.desc
        if count[image.desc] > 0:
            description += " (%i)" % (count[image.desc] + 1)
        count[image.desc] += 1
        return id3.APIC(encoding=UTF_8, mime=image.mime,
                        type=self.__METADATA_IMAGE_TYPES[image.type],
                        desc=description, data=image.data)