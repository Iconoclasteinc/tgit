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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox


class Contributor:
    def __init__(self, name="", role="", ipi="", isni=""):
        self.isni = isni
        self.ipi = ipi
        self.role = role
        self.name = name


class Cell:
    class Name(QTableWidgetItem):
        def __init__(self, contributor, ipi_item, isni_item, lookup_ipi, lookup_isni, on_name_changed):
            super().__init__()
            self._on_name_changed = on_name_changed
            self._isni_item = isni_item
            self._ipi_item = ipi_item
            self._lookup_isni = lookup_isni
            self._lookup_ipi = lookup_ipi
            self.setData(Qt.UserRole, contributor)

            if contributor.name:
                self.setText(contributor.name)

        def value_changed(self):
            name = self.text()
            contributor = self.data(Qt.UserRole)
            if contributor.name != name:
                contributor.name = name
                contributor.isni = self._lookup_isni(name)
                contributor.ipi = self._lookup_ipi(name)
                self._isni_item.setText(contributor.isni)
                self._ipi_item.setText(contributor.ipi)
                self._on_name_changed()

    class Role(QComboBox):
        def __init__(self, contributor, on_role_changed):
            super().__init__()
            self._on_role_changed = on_role_changed
            self._contributor = contributor

            self.addItems(["", self.tr("Author"), self.tr("Composer"), self.tr("Publisher")])
            self.setCurrentText(contributor.role)
            self.currentIndexChanged.connect(lambda _: self._role_changed())

        def _role_changed(self):
            self._contributor.role = self.currentText()
            self._on_role_changed()

    class IPI(QTableWidgetItem):
        def __init__(self, contributor, on_ipi_changed):
            super().__init__()
            self._on_ipi_changed = on_ipi_changed

            self.setData(Qt.UserRole, contributor)
            if contributor.ipi:
                self.setText(contributor.ipi)

        def value_changed(self):
            ipi = self.text() or None
            contributor = self.data(Qt.UserRole)
            if contributor.ipi != ipi:
                contributor.ipi = ipi
                self._on_ipi_changed(contributor.name, ipi)

    class ISNI(QTableWidgetItem):
        def __init__(self, contributor):
            super().__init__()
            self.setData(Qt.UserRole, contributor)
            self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            if contributor.isni:
                self.setText(contributor.isni)

        def value_changed(self):
            isni = self.text()
            contributor = self.data(Qt.UserRole)
            if contributor.isni != isni:
                contributor.isni = isni
