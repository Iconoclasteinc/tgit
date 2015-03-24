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

import os

from mutagen import id3

from tgit.util import fs


class MediaLibrary(object):
    def load(self, name):
        pass

    def release(self, media):
        pass


class Mp3Audio(object):
    def __init__(self, filename):
        self._filename = filename
        self._playableCopy = self._copy(filename)

    @property
    def name(self):
        return self._filename

    def source(self):
        return self._playableCopy

    def _copy(self, filename):
        # On Windows, we have 2 issues with Phonon:
        # 1- It locks the file so we have to make a copy to allow tagging
        copy = fs.makeTempCopy(filename)
        # 2- It fails to play files with our tags so we have to clear the frames
        id3.delete(filename=copy)
        return copy

    def release(self):
        os.unlink(self._playableCopy)


class AudioFiles(MediaLibrary):
    def load(self, filename):
        return Mp3Audio(filename)

    def release(self, media):
        media.release()
