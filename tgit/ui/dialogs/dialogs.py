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
from PyQt5.QtWidgets import QApplication

from tgit.ui.dialogs.isni_assignation_review_dialog import make_isni_assignation_review_dialog
from tgit.ui.dialogs.load_album_dialog import make_load_project_dialog
from tgit.ui.dialogs.save_as_dialog import make_save_as_csv_dialog, make_save_as_excel_dialog
from tgit.ui.dialogs.select_album_destination_dialog import make_select_project_destination_dialog
from tgit.ui.dialogs.track_selection_dialog import TrackSelectionDialog


class Dialogs:
    def __init__(self, native):
        self._native = native

    @property
    def _parent(self):
        return QApplication.activeWindow()

    def _select_tracks_dialog(self):
        return TrackSelectionDialog(self._parent, self._native, delete_on_close=True)

    def select_tracks(self, file_type, on_select):
        return self._select_tracks_dialog().select_files(file_type, on_select)

    def add_tracks_in_folder(self, file_type, on_select):
        return self._select_tracks_dialog().select_files_in_folder(file_type, on_select)

    def select_track(self, file_type, on_select):
        return self._select_tracks_dialog().select_file(file_type, on_select)

    def export_as_csv(self, on_select, default_file_name=""):
        return make_save_as_csv_dialog(on_select, default_file_name, self._parent, self._native).open()

    def save_as_excel(self, on_select, default_file_name=""):
        return make_save_as_excel_dialog(on_select, default_file_name, self._parent, self._native).open()

    def select_project_destination(self, on_select):
        return make_select_project_destination_dialog(on_select, self._parent, self._native).open()

    def select_project_to_load(self, on_select):
        return make_load_project_dialog(on_select, self._parent, self._native).open()

    def review_isni_assignation_in(self, album, main_artist_section_visible=False):
        def review_isni_assignation(on_review):
            make_isni_assignation_review_dialog(album.tracks, on_review, self._parent, main_artist_section_visible).open()

        return review_isni_assignation
