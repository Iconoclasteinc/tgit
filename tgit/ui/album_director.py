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
from tgit.ui.album_composer import AlbumComposer
from tgit.ui.album_editor import AlbumEditor
from tgit.ui.album_mixer import AlbumMixer
from tgit.ui.track_editor import TrackEditor
from tgit.ui.views import albumScreen


INDEX_OF_TRACK_PAGES = 2


class AlbumDirector(AlbumListener):
    def __init__(self, album, trackCatalog, player):
        self._album = album
        self._trackCatalog = trackCatalog
        self._player = player
        self._view = albumScreen(self)

    def render(self):
        widget = self._view.render()
        composer = AlbumComposer(self._album, self._player)
        composer.announceTo(self)
        # todo consider having setAlbumComposer ...
        self._view.appendPage(composer.render())
        # todo ... and setAlbumEditor
        editor = AlbumEditor(self._album)
        self._view.appendPage(editor.render())
        self._album.addAlbumListener(self)
        return widget

    # Eventually, event will bubble up to top level presenter.
    # For that we need to do some prep work on the menubar first.
    def addTracksToAlbum(self, folders=False):
        mixer = AlbumMixer(self._album, self._trackCatalog)
        mixer.show(folders=folders)

    def trackAdded(self, track, position):
        editor = TrackEditor(self._album, track)
        # todo consider having insertTrackEditor...
        self._view.insertPage(editor.render(), INDEX_OF_TRACK_PAGES + position)
        if not self._album.empty():
            self._view.allowSaves(True)

    def trackRemoved(self, track, position):
        # todo ... along with removeTrackEditor
        self._view.removePage(INDEX_OF_TRACK_PAGES + position)
        if self._album.empty():
            self._view.allowSaves(False)

    def recordAlbum(self):
        for track in self._album.tracks:
            self._trackCatalog.save(track)