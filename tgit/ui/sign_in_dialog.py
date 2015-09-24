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
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QMessageBox

from tgit.authentication_error import AuthenticationError
from tgit.ui.helpers.ui_file import UIFile


class SignInDialog(QDialog, UIFile):
    _on_sign_in = lambda: None

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self._setup_ui()

    def _setup_ui(self):
        self._load(":ui/sign_in_dialog.ui")
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._action_buttons.clicked.connect(self._button_clicked)
        self._authentication_error.setVisible(False)
        self.adjustSize()

    def sign_in(self, on_sign_in):
        self._on_sign_in = on_sign_in
        self.open()

    def _button_clicked(self, button):
        role = self._action_buttons.buttonRole(button)

        if role == QMessageBox.AcceptRole:
            try:
                self._on_sign_in(self._email.text(), self._password.text())
                self.accept()
            except AuthenticationError:
                self._authentication_error.setVisible(True)
