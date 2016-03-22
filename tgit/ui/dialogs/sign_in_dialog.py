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
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from tgit.signal import MultiSubscription
from tgit.ui.event_loop_signaler import in_event_loop
from tgit.ui.helpers.ui_file import UIFile


def make_sign_in_dialog(login, on_sign_in, parent=None, delete_on_close=True):
    dialog = SignInDialog(parent, delete_on_close)
    dialog.on_sign_in.connect(on_sign_in)
    subscriptions = MultiSubscription()
    subscriptions += login.on_start.subscribe(in_event_loop(dialog.login_in_progress))
    subscriptions += login.on_success.subscribe(in_event_loop(lambda email: dialog.login_succeeded()))
    subscriptions += login.on_failure.subscribe(in_event_loop(lambda error: dialog.login_failed()))
    dialog.finished.connect(lambda accepted: subscriptions.cancel())
    return dialog


class SignInDialog(QDialog, UIFile):
    on_sign_in = pyqtSignal(str, str)

    def __init__(self, parent=None, delete_on_close=True):
        super().__init__(parent, Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self.setAttribute(Qt.WA_DeleteOnClose, delete_on_close)
        self._setup_ui()

    def _setup_ui(self):
        self._load(":ui/sign_in_dialog.ui")
        self._email.textEdited.connect(lambda text: self._ok_button.setEnabled(len(text) > 0))
        self._buttons.accepted.connect(lambda: self.on_sign_in.emit(self._email.text(), self._password.text()))
        self._ok_button.setDisabled(True)

    def login_succeeded(self):
        self._progress_indicator.stop()
        self.accept()

    def login_in_progress(self):
        self._progress_indicator.start()
        self._ok_button.setDisabled(True)

    def login_failed(self):
        self._progress_indicator.stop()
        self._authentication_error.setText(self.tr("Invalid username and/or password"))
        self._ok_button.setEnabled(True)

    @property
    def _ok_button(self):
        return self._buttons.button(QDialogButtonBox.Ok)
