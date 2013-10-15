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

from tgit import album
from tgit.metadata import Metadata, Image

TITLE = 'trackTitle'
VERSION_INFO = 'versionInfo'
FEATURED_GUEST = 'featuredGuest'
ISRC = 'isrc'


class Track(object):
    def __init__(self, audioFile):
        self._audioFile = audioFile
        self._metadata = Metadata(audioFile.metadata)

    @property
    def filename(self):
        return self._audioFile.filename

    @property
    def bitrate(self):
        return self._audioFile.bitrate

    @property
    def duration(self):
        return self._audioFile.duration

    @property
    def releaseName(self):
        return self._metadata[album.TITLE]

    @releaseName.setter
    def releaseName(self, title):
        self._metadata[album.TITLE] = title

    @property
    def leadPerformer(self):
        return self._metadata[album.LEAD_PERFORMER]

    @leadPerformer.setter
    def leadPerformer(self, performer):
        self._metadata[album.LEAD_PERFORMER] = performer

    @property
    def guestPerformers(self):
        return self._metadata[album.GUEST_PERFORMERS]

    @guestPerformers.setter
    def guestPerformers(self, performers):
        self._metadata[album.GUEST_PERFORMERS] = performers

    @property
    def frontCoverPicture(self):
        frontCovers = self._metadata.imagesOfType(Image.FRONT_COVER)
        if frontCovers:
            return frontCovers[0].mime, frontCovers[0].data
        else:
            return None, None

    @frontCoverPicture.setter
    def frontCoverPicture(self, picture):
        self._metadata.removeImages()
        mime, data = picture
        if data:
            self._metadata.addImage(mime, data, Image.FRONT_COVER, 'Front Cover')

    @property
    def labelName(self):
        return self._metadata[album.LABEL_NAME]

    @labelName.setter
    def labelName(self, label):
        self._metadata[album.LABEL_NAME] = label

    @property
    def recordingTime(self):
        return self._metadata[album.RECORDING_TIME]

    @recordingTime.setter
    def recordingTime(self, time):
        self._metadata[album.RECORDING_TIME] = time

    @property
    def releaseTime(self):
        return self._metadata[album.RELEASE_TIME]

    @releaseTime.setter
    def releaseTime(self, time):
        self._metadata[album.RELEASE_TIME] = time

    @property
    def originalReleaseTime(self):
        return self._metadata[album.ORIGINAL_RELEASE_TIME]

    @originalReleaseTime.setter
    def originalReleaseTime(self, time):
        self._metadata[album.ORIGINAL_RELEASE_TIME] = time

    @property
    def upc(self):
        return self._metadata[album.UPC]

    @upc.setter
    def upc(self, code):
        self._metadata[album.UPC] = code

    @property
    def trackTitle(self):
        return self._metadata[TITLE]

    @trackTitle.setter
    def trackTitle(self, title):
        self._metadata[TITLE] = title

    @property
    def versionInfo(self):
        return self._metadata[VERSION_INFO]

    @versionInfo.setter
    def versionInfo(self, info):
        self._metadata[VERSION_INFO] = info

    @property
    def featuredGuest(self):
        return self._metadata[FEATURED_GUEST]

    @featuredGuest.setter
    def featuredGuest(self, guest):
        self._metadata[FEATURED_GUEST] = guest

    @property
    def isrc(self):
        return self._metadata[ISRC]

    @isrc.setter
    def isrc(self, code):
        self._metadata[ISRC] = code

    def save(self):
        self._audioFile.update(self._metadata)
        self._audioFile.save()