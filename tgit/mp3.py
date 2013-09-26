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

from mutagen.mp3 import MP3
from mutagen import id3

FEATURED_GUEST = 'Featured Guest'
UPC = 'UPC'
FRONT_COVER = 3
UTF_8 = 3


class MP3File(object):
    def __init__(self, filename):
        super(MP3File, self).__init__()
        self._mp3 = MP3(filename)

    @property
    def filename(self):
        return self._mp3.filename

    @property
    def frontCoverPicture(self):
        attachedPictures = self._framesOfType(id3.APIC)
        for pic in attachedPictures:
            if pic.type == FRONT_COVER:
                return pic.mime, pic.data

        return None, None

    @frontCoverPicture.setter
    def frontCoverPicture(self, picture):
        mimeType, imageData = picture
        if imageData is None:
            self._overwriteFrames(id3.APIC)
            return
        frontCover = id3.APIC(encoding=UTF_8, mime=mimeType, type=FRONT_COVER,
                              desc='Front Cover', data=imageData)
        self._overwriteFrames(id3.APIC, frontCover)

    @property
    def releaseName(self):
        return self._getText(id3.TALB())

    @releaseName.setter
    def releaseName(self, album):
        self._addTextFrame(id3.TALB(text=album))

    @property
    def leadPerformer(self):
        return self._getText(id3.TPE1())

    @leadPerformer.setter
    def leadPerformer(self, artist):
        self._addTextFrame(id3.TPE1(text=artist))

    @property
    def releaseDate(self):
        return self._getText(id3.TDRL())

    @releaseDate.setter
    def releaseDate(self, timestamp):
        self._addTextFrame(id3.TDRL(text=timestamp))

    @property
    def upc(self):
        return self._getText(id3.TXXX(desc=UPC))

    @upc.setter
    def upc(self, code):
        self._addTextFrame(id3.TXXX(desc=UPC, text=code))

    @property
    def trackTitle(self):
        return self._getText(id3.TIT2())

    @trackTitle.setter
    def trackTitle(self, title):
        self._addTextFrame(id3.TIT2(text=title))

    @property
    def versionInfo(self):
        return self._getText(id3.TPE4())

    @versionInfo.setter
    def versionInfo(self, info):
        self._addTextFrame(id3.TPE4(text=info))

    @property
    def featuredGuest(self):
        return self._getText(id3.TXXX(desc=FEATURED_GUEST))

    @featuredGuest.setter
    def featuredGuest(self, name):
        self._addTextFrame(id3.TXXX(desc=FEATURED_GUEST, text=name))

    @property
    def isrc(self):
        return self._getText(id3.TSRC())

    @isrc.setter
    def isrc(self, isrc):
        self._addTextFrame(id3.TSRC(text=isrc))

    @property
    def bitrate(self):
        return self._mp3.info.bitrate

    @property
    def bitrateInKbps(self):
        return int(round(self.bitrate, -3) / 1000)

    @property
    def duration(self):
        return self._mp3.info.length

    @property
    def durationAsText(self):
        minutes, seconds = divmod(round(self.duration), 60)
        return "%02d:%02d" % (minutes, seconds)

    def save(self):
        self._mp3.save()

    def _getText(self, frame):
        return self._hasFrame(frame) and self._asText(frame) or None

    def _hasFrame(self, frame):
        return self._mp3.tags and frame.HashKey in self._mp3.tags

    def _asText(self, frame):
        return unicode(self._mp3[frame.HashKey])

    def _addTextFrame(self, frame):
        frame.encoding = UTF_8
        self._addFrame(frame)

    def _addFrame(self, frame):
        if not self._mp3.tags:
            self._mp3.add_tags()
        self._mp3.tags.add(frame)

    def _overwriteFrames(self, frameType, *frames):
        self._mp3.tags.setall(self._frameId(frameType), frames)

    def _framesOfType(self, frameType):
        if self._mp3.tags:
            return self._mp3.tags.getall(self._frameId(frameType))
        else:
            return []

    def _frameId(self, frame_type):
        return frame_type.__name__
