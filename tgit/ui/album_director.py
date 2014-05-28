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


class AlbumDirector(AlbumListener):
    def __init__(self, album, trackLibrary, player, view, trackView):
        self.album = album
        self.album.addAlbumListener(self)
        self.trackLibrary = trackLibrary
        self.player = player
        self.view = view
        self.trackView = trackView

        self.bindEventHandlers()

    def bindEventHandlers(self):
        self.view.bind(recordAlbum=self.recordAlbum)

    def trackAdded(self, track, position):
        self.view.addTrackEditionPage(self.trackView(track), position)
        self.view.allowSaves(True)

    def trackRemoved(self, track, position):
        self.view.removeTrackEditionPage(position)
        if self.album.empty():
            self.view.allowSaves(False)

    def recordAlbum(self):
        for track in self.album.tracks:
            self.trackLibrary.store(track)