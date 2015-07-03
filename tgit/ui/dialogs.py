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

from tgit.ui.track_selection_dialog import TrackSelectionDialog
from tgit.ui.export_as_dialog import make_export_as_dialog
from tgit.ui.picture_selection_dialog import make_picture_selection_dialog
from tgit.ui.select_album_destination_dialog import SelectAlbumDestinationDialog
from tgit.ui.load_album_dialog import LoadAlbumDialog


class Dialogs:
    _pictures = None
    _tracks = None
    _export = None
    _select_album_destination = None
    _select_album_to_load = None

    parent = None

    def __init__(self, native):
        self._native = native

    def _select_tracks_dialog(self):
        if not self._tracks:
            self._tracks = TrackSelectionDialog(self.parent, native=self._native)

        return self._tracks

    def select_cover(self, on_select):
        if not self._pictures:
            self._pictures = make_picture_selection_dialog(self.parent, native=self._native)

        return self._pictures.select(on_select)

    def select_tracks(self, file_type, on_select):
        return self._select_tracks_dialog().select_files(file_type, on_select)

    def add_tracks_in_folder(self, file_type, on_select):
        return self._select_tracks_dialog().select_files_in_folder(file_type, on_select)

    def select_track(self, file_type, on_select):
        return self._select_tracks_dialog().select_file(file_type, on_select)

    def export(self, on_select):
        if not self._export:
            self._export = make_export_as_dialog(self.parent, native=self._native)

        return self._export.select(on_select)

    def select_album_destination(self, on_select):
        if not self._select_album_destination:
            self._select_album_destination = SelectAlbumDestinationDialog(self.parent, native=self._native)

        return self._select_album_destination.select(on_select)

    def select_album_to_load(self, on_select):
        if not self._select_album_to_load:
            self._select_album_to_load = LoadAlbumDialog(self.parent, native=self._native)

        return self._select_album_to_load.select(on_select)

    def clear(self):
        self._pictures = None
        self._tracks = None
        self._export = None
