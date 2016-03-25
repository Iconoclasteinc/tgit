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
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from tgit.album import AlbumListener
from tgit.ui.closeable import Closeable

from tgit.ui.helpers.ui_file import UIFile


def make_musician_tab(project, on_metadata_changed):
    tab = MusicianTab()
    tab.on_metadata_changed.connect(lambda metadata: on_metadata_changed(**metadata))

    # todo when we have proper signals on album, we can get rid of that
    project.addAlbumListener(tab)
    tab.closed.connect(lambda: project.removeAlbumListener(tab))

    tab.display(project)
    return tab


@Closeable
class MusicianTab(QWidget, UIFile, AlbumListener):
    closed = pyqtSignal()
    on_metadata_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._load(":/ui/musician_tab.ui")
        self._add_musician_button.clicked.connect(lambda: self._add_musician_row())

    def display(self, project):
        if self._is_empty():
            musicians = project.guest_performers if project.guest_performers is not None else []
            for musician in musicians:
                self._add_musician_row(musician)

    def albumStateChanged(self, project):
        self.display(project)

    def _is_empty(self):
        return self._musician_table.count() == 0

    def _add_musician_row(self, musician=(None, None)):
        self._musician_table.addWidget(make_musician_row(index=self._musician_table.count(), musician=musician,
                                                         on_musician_changed=self._metadata_changed,
                                                         on_musician_removed=self._metadata_changed))

    def _metadata_changed(self):
        self.on_metadata_changed.emit(dict(guest_performers=self._musicians))

    @property
    def _musicians(self):
        musicians = []
        for index in range(self._musician_table.count()):
            if self._row_is_empty(index):
                continue

            musicians.append(self._musician_table.itemAt(index).widget().musician)

        return musicians

    def _row_is_empty(self, index):
        return self._musician_table.itemAt(index) is None


def make_musician_row(index, on_musician_changed, on_musician_removed, musician):
    row = MusicianRow(index)
    row.musician_removed.connect(on_musician_removed)
    row.musician_changed.connect(on_musician_changed)
    row.display(*musician)

    return row


class MusicianRow(QWidget, UIFile):
    musician_removed = pyqtSignal()
    musician_changed = pyqtSignal()

    def __init__(self, index):
        super().__init__()
        self._load(":/ui/musician_row.ui")
        self.setObjectName("{}_{}".format(self.objectName(), index))
        self._remove_musician_button.clicked.connect(self._remove)
        self._instrument.editingFinished.connect(self._musician_changed)
        self._musician_name.editingFinished.connect(self._musician_changed)

    def display(self, instrument, musician_name):
        self._instrument.setText(instrument)
        self._musician_name.setText(musician_name)

    @property
    def musician(self):
        return self._instrument.text(), self._musician_name.text()

    def _remove(self):
        self.setParent(None)
        self.close()
        self.musician_removed.emit()

    def _musician_changed(self):
        if self._instrument.text() and self._musician_name.text():
            self.musician_changed.emit()
