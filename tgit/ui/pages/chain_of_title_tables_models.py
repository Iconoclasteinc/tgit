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

from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QComboBox

from tgit.signal import signal

from tgit.ui.pages.table_model import Columns, Column


class Contributor:
    def __init__(self, **contributor):
        self.share = contributor.get("share", "")
        self.name = contributor["name"]


class AuthorComposer(Contributor):
    def __init__(self, **contributor):
        super().__init__(**contributor)
        self.publisher = contributor.get("publisher", "")
        self.affiliation = contributor.get("affiliation", "")


class Cell:
    class Name(QTableWidgetItem):
        def __init__(self, contributor):
            super().__init__()
            self.setData(Qt.UserRole, contributor)
            self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.setText(contributor.name)

        def value_changed(self):
            name = self.text()
            contributor = self.data(Qt.UserRole)
            if contributor.name != name:
                contributor.name = name

    class Publisher(QComboBox):
        on_publisher_changed = pyqtSignal(AuthorComposer)

        def __init__(self, contributor, items):
            super().__init__()
            self._contributor = contributor
            self.addItem("")
            self.addItems(items)
            self.setCurrentText(contributor.publisher)
            self.currentIndexChanged.connect(lambda _: self._publisher_changed())

        def _publisher_changed(self):
            self._contributor.publisher = self.currentText()
            self.on_publisher_changed.emit(self._contributor)

    class Affiliation(QComboBox):
        on_affiliation_changed = pyqtSignal(AuthorComposer)

        def __init__(self, contributor, items):
            super().__init__()
            self._contributor = contributor
            self.addItem("")
            self.addItems(items)
            self.setCurrentText(contributor.affiliation)
            self.currentIndexChanged.connect(lambda _: self._affiliation_changed())

        def _affiliation_changed(self):
            self._contributor.affiliation = self.currentText()
            self.on_affiliation_changed.emit(self._contributor)

    class Share(QTableWidgetItem):
        on_share_changed = signal(Contributor)

        def __init__(self, contributor):
            super().__init__()
            self.setData(Qt.UserRole, contributor)
            self.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setText(contributor.share)

        def value_changed(self):
            share = self.text()
            contributor = self.data(Qt.UserRole)
            if contributor.share != share:
                contributor.share = share
                self.on_share_changed.emit(contributor)


class AuthorsComposersColumns(Columns):
    name = Column(position=0, resize_mode=QHeaderView.Stretch)
    affiliation = Column(position=1)
    publisher = Column(position=2)
    share = Column(position=3)


class PublishersColumns(Columns):
    name = Column(position=0, resize_mode=QHeaderView.Stretch)
    share = Column(position=1)


affiliations = ["SOCAN", "ASCAP", "BMI"]
