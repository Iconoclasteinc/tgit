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

from tgit.util import fs


class AlbumEditor(AlbumListener):
    def __init__(self, album, page, pictureSelector):
        self.album = album
        self.album.addAlbumListener(self)
        self.view = page
        self.pictureSelector = pictureSelector

        self.bindEventHandlers()

    def bindEventHandlers(self):
        self.view.bind(metadataChanged=self.updateAlbum, selectPicture=self.selectPicture,
                       removePicture=self.removeAlbumCover)
        self.pictureSelector.bind(pictureSelected=self.changeAlbumCover)

    def render(self):
        self.refresh()
        return self.view

    def refresh(self):
        self.view.display(self.album)

    def albumStateChanged(self, album):
        self.refresh()

    def updateAlbum(self, state):
        self.album.releaseName = state.releaseName
        self.album.compilation = state.compilation
        self.album.leadPerformer = state.leadPerformer
        self.album.guestPerformers = state.guestPerformers
        self.album.labelName = state.labelName
        self.album.catalogNumber = state.catalogNumber
        self.album.upc = state.upc
        self.album.comments = state.comments
        self.album.releaseTime = state.releaseTime
        self.album.recordingTime = state.recordingTime
        self.album.recordingStudios = state.recordingStudios
        self.album.producer = state.producer
        self.album.mixer = state.mixer
        self.album.primaryStyle = state.primaryStyle

    def selectPicture(self):
        self.pictureSelector.show()

    def changeAlbumCover(self, filename):
        self.album.removeImages()
        mime, data = fs.guessMimeType(filename), fs.readContent(filename)
        self.album.addFrontCover(mime, data)

    def removeAlbumCover(self):
        self.album.removeImages()