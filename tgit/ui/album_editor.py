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
from tgit.album import AlbumListener

from tgit.ui.views import albumEditionPage, pictureSelectionDialog
from tgit.util import fs


class AlbumEditor(AlbumListener):
    def __init__(self, album):
        self._album = album
        self._page = albumEditionPage(self)
        self._pictureDialog = pictureSelectionDialog(self)

    def render(self):
        widget = self._page.render()
        self._page.show(self._album)
        self._album.addAlbumListener(self)
        return widget

    def albumStateChanged(self, state):
        self._page.show(state)

    def metadataEdited(self, state):
        self._album.releaseName = state.releaseName
        self._album.leadPerformer = state.leadPerformer
        self._album.guestPerformers = state.guestPerformers
        self._album.labelName = state.labelName
        self._album.catalogNumber = state.catalogNumber
        self._album.upc = state.upc
        self._album.comments = state.comments
        self._album.releaseTime = state.releaseTime
        self._album.recordingTime = state.recordingTime
        self._album.recordingStudios = state.recordingStudios
        self._album.producer = state.producer
        self._album.mixer = state.mixer

    def addPicture(self):
        self._pictureDialog.render()
        self._pictureDialog.show()

    def pictureSelected(self, filename):
        self._album.removeImages()
        mime, data = loadImage(filename)
        self._album.addFrontCover(mime, data)

    def removePicture(self):
        self._album.removeImages()


def loadImage(filename):
        return fs.guessMimeType(filename), fs.readContent(filename)