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


class MenuBar(object):
    FILE_MENU_NAME = 'file'
    ADD_FILES_ACTION_NAME = 'add files'
    ADD_FOLDER_ACTION_NAME = 'add folder'
    EXPORT_ACTION_NAME = 'export'

    def __init__(self):
        self._announce = Announcer()

    def bind(self, **eventHandlers):
        if 'settings' in eventHandlers:
            self.preferences.triggered.connect(eventHandlers['settings'])

    def announceTo(self, listener):
        self._announce.addListener(listener)

    def render(self):
        self._widget = self._assemble()
        self.localize()
        return self._widget

    def _assemble(self):
        menuBar = QMenuBar()
        menuBar.addMenu(self._makeFileMenu(menuBar))
        return menuBar

    def _makeFileMenu(self, menuBar):
        self._fileMenu = QMenu(menuBar)
        self._fileMenu.setObjectName(self.FILE_MENU_NAME)
        self._addAddFilesMenuItemTo(self._fileMenu)
        self._addAddFolderMenuItemTo(self._fileMenu)
        self._addExportMenuItemTo(self._fileMenu)
        self.preferences = QAction(self._fileMenu)
        self._fileMenu.addAction(self.preferences)
        return self._fileMenu

    def _addAddFilesMenuItemTo(self, menu):
        self._addFilesAction = QAction(menu)
        self._addFilesAction.setObjectName(self.ADD_FILES_ACTION_NAME)
        self._addFilesAction.triggered.connect(lambda checked: self._announce.addFiles())
        self._addFilesAction.setDisabled(True)
        menu.addAction(self._addFilesAction)

    def _addAddFolderMenuItemTo(self, menu):
        self._addFolderAction = QAction(menu)
        self._addFolderAction.setObjectName(self.ADD_FOLDER_ACTION_NAME)
        self._addFolderAction.triggered.connect(lambda checked: self._announce.addFolder())
        self._addFolderAction.setDisabled(True)
        menu.addAction(self._addFolderAction)

    def _addExportMenuItemTo(self, menu):
        self._exportMenuAction = QAction(menu)
        self._exportMenuAction.setObjectName(self.EXPORT_ACTION_NAME)
        self._exportMenuAction.triggered.connect(
            lambda checked: self._announce.export())
        self._exportMenuAction.setDisabled(True)
        menu.addAction(self._exportMenuAction)

    def enableAlbumMenu(self):
        for action in [self._addFilesAction, self._addFolderAction, self._exportMenuAction]:
            action.setEnabled(True)

    def localize(self):
        self._fileMenu.setTitle(self.tr('File'))
        self._addFilesAction.setText(self.tr('Add Files...'))
        self._addFolderAction.setText(self.tr('Add Folder...'))
        self._exportMenuAction.setText(self.tr('Export...'))
        self.preferences.setText(self.tr('Settings'))

    def tr(self, text):
        return self._widget.tr(text)