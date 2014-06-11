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
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog, QComboBox, QGridLayout, QDialogButtonBox, QLabel


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.build()

    def build(self):
        self.setObjectName('settings-dialog')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(self.tr('Settings'))
        self.setModal(True)
        layout = QGridLayout()
        label = QLabel(self.tr('&Language'))
        self.languages = QComboBox()
        self.languages.setObjectName('language')
        label.setBuddy(self.languages)
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.languages, 0, 1)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(self.buttons, 1, 0, 1, 2)
        self.setLayout(layout)

    def bind(self, **handlers):
        if 'ok' in handlers:
            self.buttons.accepted.connect(handlers['ok'])
        if 'cancel' in handlers:
            self.buttons.rejected.connect(handlers['cancel'])

    def addLanguage(self, locale, language):
        self.languages.addItem(self.tr(language), locale)

    @property
    def settings(self):
        return {'language': self.languages.itemData(self.languages.currentIndex())}

    def display(self, **settings):
        if 'language' in settings:
            self.languages.setCurrentIndex(self.languages.findData(settings['language']))
        self.show()