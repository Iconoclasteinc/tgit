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

from tgit import fs
from tgit import mp3_file as mp3
from tgit.metadata import Metadata


class MediaLibrary(object):
    def load(self, name):
        pass

    def release(self, media):
        pass


class MediaFile(object):
    def __init__(self, name, filename):
        self._name = name
        self._filename = filename

    @property
    def name(self):
        return self._name

    def source(self):
        return self._filename

    def delete(self):
        os.unlink(self._filename)


class Mp3Files(MediaLibrary):
    def load(self, name):
        # On Windows, we have 2 issues with Phonon:
        # 1- It locks the file so we have to make a copy to allow tagging
        # 2- It fails to play files with our tags so we have to clear the frames
        copy = fs.makeCopy(name)
        mp3.save(metadata=Metadata(), overwrite=True, filename=copy)
        return MediaFile(name, copy)

    def release(self, media):
        media.delete()
