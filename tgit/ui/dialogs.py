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

from tgit.ui.reference_track_selection_dialog import make_reference_track_selection_dialog
from tgit.ui.export_as_dialog import make_export_as_dialog
from tgit.ui.picture_selection_dialog import make_picture_selection_dialog
from tgit.ui.select_album_destination_dialog import SelectAlbumDestinationDialog
from tgit.ui.track_selection_dialog import make_track_selection_dialog
from tgit.ui.load_dialog import make_load_album_dialog


class Dialogs:
    _pictures = None
    _tracks = None
    _select_reference_track = None
    _export = None
    _select_album_destination = None
    _load = None

    parent = None

    def __init__(self, commands, native):
        self._commands = commands
        self._native = native

    def _select_cover_dialog(self, album):
        if not self._pictures:
            self._pictures = make_picture_selection_dialog(self.parent, native=self._native,
                                                           on_select_picture=self._commands.change_cover_of(album))

        return self._pictures

    def _select_tracks_dialog(self, album):
        if not self._tracks:
            self._tracks = make_track_selection_dialog(self.parent, native=self._native,
                                                       on_select_tracks=self._commands.add_tracks_to(album))

        return self._tracks

    def _select_reference_track_dialog(self):
        if not self._select_reference_track:
            self._select_reference_track = make_reference_track_selection_dialog(self.parent, native=self._native)

        return self._select_reference_track

    def _export_as_dialog(self, album):
        if not self._export:
            self._export = make_export_as_dialog(self.parent, native=self._native,
                                                 on_export_as=self._commands.export_as_csv(album))

        return self._export

    def _select_album_destination_dialog(self):
        if not self._select_album_destination:
            self._select_album_destination = SelectAlbumDestinationDialog(self.parent, native=self._native)

        return self._select_album_destination

    def _load_dialog(self, album_portfolio):
        if not self._load:
            self._load = make_load_album_dialog(self.parent, native=self._native,
                                                on_select_album=self._commands.load_album_into(album_portfolio))

        return self._load

    def select_cover(self, album):
        return self._select_cover_dialog(album)

    def add_tracks(self, album):
        dialog = self._select_tracks_dialog(album)
        dialog.select_files()
        dialog.filter_tracks(album.type)
        return dialog

    def add_tracks_in_folder(self, album):
        dialog = self._select_tracks_dialog(album)
        dialog.select_folders()
        dialog.filter_tracks(album.type)
        return dialog

    def select_reference_track(self):
        return self._select_reference_track_dialog().display

    def export(self, album):
        return self._export_as_dialog(album)

    def select_album_destination(self):
        return self._select_album_destination_dialog().display

    def load_album_file(self, album_portfolio):
        return self._load_dialog(album_portfolio)

    def clear(self):
        self._pictures = None
        self._tracks = None
        self._export = None
