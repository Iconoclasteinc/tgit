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


from PyQt4.QtGui import QMenuBar, QMenu, QAction

from tgit.announcer import Announcer
from tgit.ui import constants as ui


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        QMenuBar.__init__(self, parent)

        self._announce = Announcer()
        self._assemble()
        self.localize()

    def announceTo(self, listener):
        self._announce.addListener(listener)

    def albumCreated(self, album):
        self._updateAlbumMenu(album)

    def _assemble(self):
        self.addMenu(self._makeFileMenu())

    def _makeFileMenu(self):
        self._fileMenu = QMenu(self)
        self._fileMenu.setObjectName(ui.FILE_MENU_NAME)
        self._addAddFilesMenuItemTo(self._fileMenu)
        self._addAddFolderMenuItemTo(self._fileMenu)
        self._addExportMenuItemTo(self._fileMenu)
        return self._fileMenu

    def _addAddFilesMenuItemTo(self, menu):
        self._addFilesAction = QAction(menu)
        self._addFilesAction.setObjectName(ui.ADD_FILES_ACTION_NAME)
        self._addFilesAction.triggered.connect(lambda checked: self._announce.selectFiles())
        self._addFilesAction.setDisabled(True)
        menu.addAction(self._addFilesAction)

    def _addAddFolderMenuItemTo(self, menu):
        self._addFolderAction = QAction(menu)
        self._addFolderAction.setObjectName(ui.ADD_FOLDER_ACTION_NAME)
        self._addFolderAction.triggered.connect(lambda checked: self._announce.selectFolder())
        self._addFolderAction.setDisabled(True)
        menu.addAction(self._addFolderAction)

    def _addExportMenuItemTo(self, menu):
        self._exportMenuAction = QAction(menu)
        self._exportMenuAction.setObjectName(ui.EXPORT_ACTION_NAME)
        self._exportMenuAction.triggered.connect(
            lambda checked: self._announce.export(self._exportMenuAction.data()))
        self._exportMenuAction.setDisabled(True)
        menu.addAction(self._exportMenuAction)

    def _updateAlbumMenu(self, album):
        for action in [self._addFilesAction, self._addFolderAction, self._exportMenuAction]:
            action.setData(album)
            action.setEnabled(True)

    def localize(self):
        self._fileMenu.setTitle(self.tr('File'))
        self._addFilesAction.setText(self.tr('Add Files...'))
        self._addFolderAction.setText(self.tr('Add Folder...'))
        self._exportMenuAction.setText(self.tr('Export...'))