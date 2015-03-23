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
from PyQt4.QtCore import pyqtSignal

from PyQt4.QtGui import QMenuBar, QMenu, QAction
from tgit4.album import Album


class MenuBar(QMenuBar):
    addFiles = pyqtSignal(Album)
    addFolder = pyqtSignal(Album)
    export = pyqtSignal(Album)
    settings = pyqtSignal()

    def __init__(self):
        QMenuBar.__init__(self)
        self.albumActions = []
        self.build()

    def albumCreated(self, album):
        for action in self.albumActions:
            action.setEnabled(True)
            action.setData(album)

    def build(self):
        self.addMenu(self.makeFileMenu())

    def makeFileMenu(self):
        menu = QMenu(self)
        menu.setObjectName('file-menu')
        menu.setTitle(self.tr('File'))
        self.appendAddFilesItem(menu)
        self.appendAddFolderItem(menu)
        self.appendExportItem(menu)
        self.appendPreferencesItem(menu)
        return menu

    def appendAddFilesItem(self, menu):
        action = QAction(menu)
        action.setObjectName('add-files')
        action.setText(self.tr('Add Files...'))
        action.setDisabled(True)
        action.triggered.connect(lambda checked: self.addFiles.emit(action.data()))
        menu.addAction(action)
        self.albumActions.append(action)

    def appendAddFolderItem(self, menu):
        action = QAction(menu)
        action.setObjectName('add-folder')
        action.setText(self.tr('Add Folder...'))
        action.setDisabled(True)
        action.triggered.connect(lambda checked: self.addFolder.emit(action.data()))
        menu.addAction(action)
        self.albumActions.append(action)

    def appendExportItem(self, menu):
        action = QAction(menu)
        action.setObjectName('export')
        action.setText(self.tr('Export...'))
        action.setDisabled(True)
        action.triggered.connect(lambda checked: self.export.emit(action.data()))
        menu.addAction(action)
        self.albumActions.append(action)

    def appendPreferencesItem(self, menu):
        action = QAction(menu)
        action.setObjectName('Settings')
        action.setText(self.tr('Settings'))
        action.triggered.connect(lambda checked: self.settings.emit())
        menu.addAction(action)
