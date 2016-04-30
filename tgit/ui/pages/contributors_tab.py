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
from tgit.ui.pages.contributors_table import ContributorsTable
from tgit.ui.pages.contributors_table_model import Contributor


def make_contributors_tab(project, track, on_metadata_changed, on_isni_local_lookup, on_ipi_local_lookup,
                          on_ipi_changed):
    tab = ContributorsTab(on_isni_local_lookup, on_ipi_local_lookup)
    tab.display(track)
    tab.on_metadata_changed.connect(lambda metadata: on_metadata_changed(**metadata))
    tab.on_ipi_changed.connect(on_ipi_changed)

    # todo when we have proper signals on album, we can get rid of that
    project.addAlbumListener(tab)
    tab.closed.connect(lambda: project.removeAlbumListener(tab))

    return tab


@Closeable
class ContributorsTab(QWidget, UIFile, AlbumListener):
    closed = pyqtSignal()
    on_metadata_changed = pyqtSignal(dict)
    on_ipi_changed = pyqtSignal(str, str)

    def __init__(self, on_isni_local_lookup, on_ipi_local_lookup):
        super().__init__()
        self._load(":/ui/contributors_tab.ui")
        self._table = ContributorsTable(self._contributors_table, on_ipi_local_lookup, on_isni_local_lookup)
        self._table.on_contributors_changed.connect(self._metadata_changed)
        self._table.on_contributors_changed.connect(self._disable_remove_button)
        self._table.on_contributor_selected.connect(self._enable_remove_button)
        self._table.on_ipi_changed.connect(self.on_ipi_changed.emit)
        self._add_button.clicked.connect(self._table.add_row)
        self._remove_button.clicked.connect(self._table.remove_row)

    def display(self, track):
        self._table.display(track)

    def albumStateChanged(self, project):
        self._table.update_identifiers(project.ipis or {}, project.isnis or {})

    def _enable_remove_button(self):
        self._remove_button.setEnabled(self._contributors_table.currentRow() > -1)

    def _disable_remove_button(self, contributors):
        if len(contributors) == 0:
            self._remove_button.setEnabled(False)

    def _metadata_changed(self, contributors):
        metadata = dict(lyricist=[], composer=[], publisher=[])
        for contributor in contributors:
            if contributor.role == self.tr(Contributor.AUTHOR):
                metadata["lyricist"].append(contributor.name)

            if contributor.role == self.tr(Contributor.COMPOSER):
                metadata["composer"].append(contributor.name)

            if contributor.role == self.tr(Contributor.PUBLISHER):
                metadata["publisher"].append(contributor.name)

        self.on_metadata_changed.emit(metadata)
