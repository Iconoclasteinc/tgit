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

from tgit.identity import IdentityCard
from tgit.signal import MultiSubscription
from tgit.ui.event_loop_signaler import in_event_loop
from tgit.ui.helpers.ui_file import UIFile


def make_isni_assignation_review_dialog(selection, on_assign, parent=None, delete_on_close=True):
    dialog = ISNIAssignationReviewDialog(parent, delete_on_close)

    subscriptions = MultiSubscription()
    subscriptions += selection.on_assignation_start.subscribe(in_event_loop(dialog.assignation_in_progress))
    subscriptions += selection.on_success.subscribe(in_event_loop(dialog.assignation_succeeded))
    subscriptions += selection.on_connection_failed.subscribe(in_event_loop(dialog.connection_failed))
    subscriptions += selection.on_insufficient_information.subscribe(in_event_loop(dialog.insufficient_information))

    dialog.on_assign.connect(on_assign)
    dialog.finished.connect(lambda accepted: subscriptions.cancel())

    dialog.display(selection)
    return dialog


class ISNIAssignationReviewDialog(QDialog, UIFile):
    on_assign = pyqtSignal(str)

    def __init__(self, parent, delete_on_close):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, delete_on_close)
        self._setup_ui()

    def _setup_ui(self):
        self._load(":ui/isni_assignation_review_dialog.ui")
        self._hide_messages()
        self._ok_button.clicked.connect(lambda: self.on_assign.emit(self._type))

    def display(self, selection):
        self._name.setText(selection.query)
        self._works.addItems(selection.works)

    def assignation_in_progress(self):
        self._progress_indicator.start()
        self._ok_button.setDisabled(True)

    def assignation_succeeded(self):
        self._progress_indicator.stop()
        self.accept()

    def connection_failed(self):
        self._stop_waiting()
        self._connection_error_message.setVisible(True)

    def insufficient_information(self):
        self._stop_waiting()
        self._insufficient_error_message.setVisible(True)

    def _stop_waiting(self):
        self._progress_indicator.stop()
        self._ok_button.setEnabled(True)

    def _hide_messages(self):
        self._connection_error_message.setVisible(False)
        self._insufficient_error_message.setVisible(False)

    @property
    def _type(self):
        return IdentityCard.INDIVIDUAL if self._individual_button.isChecked() else IdentityCard.ORGANIZATION

    @property
    def _ok_button(self):
        return self._action_buttons.button(QDialogButtonBox.Ok)
