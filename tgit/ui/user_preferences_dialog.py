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

from PyQt5.QtCore import Qt, pyqtSignal, QLocale
from PyQt5.QtWidgets import QDialog, QComboBox, QGridLayout, QDialogButtonBox, QLabel


def open_user_preferences_dialog(preferences, show_restart_message, on_preferences_changed):
    dialog = UserPreferencesDialog()
    dialog.on_preferences_changed(on_preferences_changed)
    dialog.on_preferences_changed(lambda prefs: show_restart_message())
    dialog.display(preferences)
    return dialog


class UserPreferencesDialog(QDialog):
    preferences_changed = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self._setup_ui()

    def _setup_ui(self):
        self.setObjectName('user_preferences_dialog')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(self.tr('Settings'))
        self.setModal(True)
        layout = QGridLayout()
        label = QLabel(self.tr('&Language:'))
        self.languages = QComboBox()
        self.languages.setObjectName('language')
        label.setBuddy(self.languages)
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.languages, 0, 1)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(lambda: self.preferences_changed.emit(self.preferences))
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons, 1, 0, 1, 2)
        self.setLayout(layout)

        self.add_language("en", "English")
        self.add_language("fr", "Français")

    def add_language(self, locale, language):
        self.languages.addItem(language, locale)

    def on_preferences_changed(self, handler):
        self.preferences_changed.connect(handler)

    @property
    def preferences(self):
        return {'locale': self.languages.itemData(self.languages.currentIndex())}

    def display(self, user_preferences):
        self.languages.setCurrentText(QLocale(user_preferences.locale).nativeLanguageName().capitalize())
        self.show()
