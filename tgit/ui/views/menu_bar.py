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


class MenuBar(QMenuBar):
    def __init__(self):
        QMenuBar.__init__(self)
        self.render()

    def bind(self, **handlers):
        if 'settings' in handlers:
            self.preferences.triggered.connect(lambda checked: handlers['settings']())
        if 'addFiles' in handlers:
            self.addFiles.triggered.connect(lambda checked: handlers['addFiles']())
        if 'addFolder' in handlers:
            self.addFolder.triggered.connect(lambda checked: handlers['addFolder']())
        if 'exportAlbum' in handlers:
            self.export.triggered.connect(lambda checked: handlers['exportAlbum']())

    def render(self):
        self.addMenu(self.makeFileMenu())
        return self

    def makeFileMenu(self):
        menu = QMenu(self)
        menu.setObjectName('file-menu')
        menu.setTitle(self.tr('File'))

        self.addFiles = QAction(menu)
        self.addFiles.setObjectName('add-files')
        self.addFiles.setText(self.tr('Add Files...'))
        self.addFiles.setDisabled(True)
        menu.addAction(self.addFiles)

        self.addFolder = QAction(menu)
        self.addFolder.setObjectName('add-folder')
        self.addFolder.setText(self.tr('Add Folder...'))
        self.addFolder.setDisabled(True)
        menu.addAction(self.addFolder)

        self.export = QAction(menu)
        self.export.setObjectName('export')
        self.export.setText(self.tr('Export...'))
        self.export.setDisabled(True)
        menu.addAction(self.export)

        self.preferences = QAction(menu)
        self.preferences.setObjectName('Settings')
        self.preferences.setText(self.tr('Settings'))
        menu.addAction(self.preferences)

        return menu

    def enableAlbumActions(self):
        for action in [self.addFiles, self.addFolder, self.export]:
            action.setEnabled(True)