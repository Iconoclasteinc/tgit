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
from io import BytesIO

from PyQt5 import uic
from PyQt5.QtCore import QFile
from PyQt5.QtCore import QIODevice

# noinspection PyUnresolvedReferences
from . import resources_rc


def load(path):
    file = QFile(path)
    try:
        file.open(QIODevice.ReadOnly)
        return file.readAll()
    finally:
        file.close()


def stream(path):
    return BytesIO(load(path))


class Loader:
    def __init__(self, path):
        self._ui_factory = uic.loadUiType(stream(path), from_imports=True)[0]

    def create(self, widget):
        ui = self._ui_factory()
        ui.setupUi(widget)
        return ui


welcome_page = Loader(":/ui/welcome_page.ui")
