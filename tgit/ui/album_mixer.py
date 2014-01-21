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

from PyQt4.QtCore import QDir, QFileInfo
from tgit.ui.views.track_selection_dialog import trackSelectionDialog


class AlbumMixer(object):
    MP3_FILES = '*.mp3'

    def __init__(self, album, catalog):
        self._album = album
        self._trackCatalog = catalog

    def show(self, folders=False):
        dialog = trackSelectionDialog(self)
        dialog.filter = AlbumMixer.MP3_FILES
        dialog.render(folderMode=folders)

    def tracksSelected(self, selection):
        for filename in self._listFilesIn(selection):
            self._album.addTrack(self._trackCatalog.load(filename))

    def _listFilesIn(self, selection):
        files = []
        for filename in selection:
            if isDir(filename):
                files.extend(self._folderContent(QDir(filename)))
            else:
                files.append(filename)
        return files

    @staticmethod
    def _folderContent(folder):
        return [f.canonicalFilePath() for f in QDir(folder).entryInfoList([AlbumMixer.MP3_FILES])]


def isDir(filename):
    return QFileInfo(filename).isDir()