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

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox, QHeaderView

from tgit.signal import signal
from tgit.ui.pages.table_model import Column, Columns


class Contributor:
    AUTHOR = "Author"
    COMPOSER = "Composer"
    PUBLISHER = "Publisher"

    def __init__(self, name="", role="", ipi="", isni=""):
        self.isni = isni
        self.ipi = ipi
        self.role = role
        self.name = name


class Cell:
    class Name(QTableWidgetItem):
        on_name_changed = signal(str)

        def __init__(self, contributor):
            super().__init__()
            self.setData(Qt.UserRole, contributor)
            self.setText(contributor.name)

        def value_changed(self):
            name = self.text()
            contributor = self.data(Qt.UserRole)
            if contributor.name != name:
                contributor.name = name
                self.on_name_changed.emit(name)

    class Role(QComboBox):
        on_role_changed = pyqtSignal()

        def __init__(self, contributor, items):
            super().__init__()
            self._contributor = contributor
            self.addItems(items)
            self.setCurrentText(contributor.role)
            self.currentIndexChanged.connect(lambda _: self._role_changed())

        def _role_changed(self):
            self._contributor.role = self.currentText()
            self.on_role_changed.emit()

    class IPI(QTableWidgetItem):
        on_ipi_changed = signal(str, str)

        def __init__(self, contributor, lookup_ipi):
            super().__init__()
            self._lookup_ipi = lookup_ipi
            self.setData(Qt.UserRole, contributor)
            self.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setText(contributor.ipi)

        def name_changed(self, name):
            contributor = self.data(Qt.UserRole)
            contributor.ipi = self._lookup_ipi(name)
            self.setText(contributor.ipi)

        def value_changed(self):
            ipi = self.text()
            contributor = self.data(Qt.UserRole)
            if contributor.ipi != ipi:
                contributor.ipi = ipi
                self.on_ipi_changed.emit(contributor.name, ipi)

    class ISNI(QTableWidgetItem):
        def __init__(self, contributor, lookup_isni):
            super().__init__()
            self._lookup_isni = lookup_isni
            self.setData(Qt.UserRole, contributor)
            self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setText(contributor.isni)

        def name_changed(self, name):
            contributor = self.data(Qt.UserRole)
            contributor.isni = self._lookup_isni(name)
            self.setText(contributor.isni)

        def value_changed(self):
            isni = self.text()
            contributor = self.data(Qt.UserRole)
            if contributor.isni != isni:
                contributor.isni = isni


class ContributorsColumns(Columns):
    name = Column(position=0, resize_mode=QHeaderView.Stretch)
    role = Column(position=1, mac_width=160, win_width=120, resize_mode=QHeaderView.Fixed)
    ipi = Column(position=2, mac_width=105, win_width=80, resize_mode=QHeaderView.Fixed)
    isni = Column(position=3, mac_width=160, win_width=140, resize_mode=QHeaderView.Fixed)
