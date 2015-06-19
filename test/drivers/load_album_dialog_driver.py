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

from PyQt5.QtWidgets import QFileDialog

from cute.matchers import named, disabled
from cute.widgets import window, FileDialogDriver


def load_album_dialog(parent):
    return LoadAlbumDialogDriver(window(QFileDialog, named("load_album_dialog")), parent.prober, parent.gesture_performer)


class LoadAlbumDialogDriver(FileDialogDriver):
    def load(self, filename):
        self.is_active()
        self.show_hidden_files()
        self.navigate_to_dir(os.path.dirname(filename))
        self.select_file(os.path.basename(filename))
        self.accept()

    def rejects_selection_of(self, filename):
        self.is_active()
        self.navigate_to_dir(os.path.dirname(filename))
        self.select_file(os.path.basename(filename))
        self.has_accept_button(disabled())
        self.reject()
