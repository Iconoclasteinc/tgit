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

from PyQt5.QtWidgets import QFrame

import tgit
from tgit.ui.helpers.ui_file import UIFile
from tgit.ui.rescue import rescue


def make_welcome_page(select_album, show_load_error, **handlers):
    page = WelcomePage(select_album=select_album, show_load_error=show_load_error)

    for name, handler in handlers.items():
        getattr(page, name)(handler)

    return page


class WelcomePage(QFrame, UIFile):
    def __init__(self, select_album, show_load_error):
        super().__init__()
        self._select_album = select_album
        self._show_load_error = show_load_error
        self._setup_ui()

    def _setup_ui(self):
        self._load(":/ui/welcome_page.ui")
        self._version_label.setText(tgit.__version__)

    def on_create_album(self, on_create_album):
        self._new_album_button.clicked.connect(on_create_album)

    def on_load_album(self, on_load_album):
        def try_loading_album(filename):
            with rescue(on_error=self._show_load_error):
                on_load_album(filename)

        self._load_album_button.clicked.connect(lambda: self._select_album(try_loading_album))
