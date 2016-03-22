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

from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtWidgets import QDialog

from tgit.ui.helpers.ui_file import UIFile


def make_user_preferences_dialog(preferences, show_restart_message, on_preferences_changed, parent=None,
                                 delete_on_close=True):
    dialog = UserPreferencesDialog(parent, delete_on_close)
    dialog.on_preferences_changed(on_preferences_changed)
    dialog.on_preferences_changed(lambda prefs: show_restart_message())
    dialog.display(preferences)
    return dialog


class UserPreferencesDialog(QDialog, UIFile):
    def __init__(self, parent, delete_on_close):
        super().__init__(parent, Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self.setAttribute(Qt.WA_DeleteOnClose, delete_on_close)
        self._setup_ui()

    def _setup_ui(self):
        self._load(":/ui/settings_dialog.ui")
        self._add_language("en", "English")
        self._add_language("fr", "Français")

    def _add_language(self, locale, language):
        self._language.addItem(language, locale)

    def on_preferences_changed(self, handler):
        self._buttons.accepted.connect(lambda: handler(self.preferences))

    @property
    def preferences(self):
        return {'locale': self._language.itemData(self._language.currentIndex())}

    def display(self, user_preferences):
        self._language.setCurrentText(QLocale(user_preferences.locale).nativeLanguageName().capitalize())
