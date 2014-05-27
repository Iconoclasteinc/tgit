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
from tgit.ui.views.album_composition_page import AlbumCompositionPage
from tgit.ui.views.album_edition_page import AlbumEditionPage
from tgit.ui.views.picture_selection_dialog import PictureSelectionDialog
from tgit.ui.views.track_edition_page import TrackEditionPage
from tgit.ui.views.track_selection_dialog import TrackSelectionDialog


class AlbumDirector(AlbumListener):
    def __init__(self, album, trackLibrary, player, view):
        self.album = album
        self.trackLibrary = trackLibrary
        self.player = player
        self.view = view

        self.bindEventHandlers()

    def bindEventHandlers(self):
        self.view.bind(recordAlbum=self.recordAlbum)

    def render(self):
        composer = AlbumComposer(self.album, self.player, AlbumCompositionPage())
        composer.onAddTracks(self.addTracksToAlbum)
        self.view.setAlbumCompositionPage(composer.render())

        editor = AlbumEditor(self.album, AlbumEditionPage(), PictureSelectionDialog())
        self.view.setAlbumEditionPage(editor.render())
        self.album.addAlbumListener(self)

        self.mixer = AlbumMixer(self.album, self.trackLibrary, TrackSelectionDialog())

        return self.view

    # Eventually, event will bubble up to top level presenter.
    # For that we need to do some prep work on the menubar first.
    def addTracksToAlbum(self, folders=False):
        self.mixer.select(folders)

    def trackAdded(self, track, position):
        editor = TrackEditor(track, TrackEditionPage())
        self.view.addTrackEditionPage(editor.render(), position)
        self.view.allowSaves(True)

    def trackRemoved(self, track, position):
        self.view.removeTrackEditionPage(position)
        if self.album.empty():
            self.view.allowSaves(False)

    def recordAlbum(self):
        for track in self.album.tracks:
            self.trackLibrary.store(track)
