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
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QListWidgetItem

from tgit.identity import IdentityCard
from tgit.signal import MultiSubscription
from tgit.ui.event_loop_signaler import in_event_loop
from tgit.ui.helpers.ui_file import UIFile


def make_isni_lookup_dialog(parent, identity_lookup, delete_on_close=True, **handlers):
    dialog = ISNILookupDialog(parent, delete_on_close)

    subscriptions = MultiSubscription()
    subscriptions += identity_lookup.on_identities_available.subscribe(in_event_loop(dialog.lookup_successful))
    subscriptions += identity_lookup.on_failed.subscribe(in_event_loop(dialog.lookup_failed))
    subscriptions += identity_lookup.on_started.subscribe(in_event_loop(dialog.lookup_in_progress))

    if "on_lookup" in handlers:
        dialog.on_lookup.connect(handlers["on_lookup"])
    dialog.on_selected.connect(identity_lookup.identity_selected)
    dialog.finished.connect(lambda accepted: subscriptions.cancel())

    return dialog


class ISNILookupDialog(QDialog, UIFile):
    on_lookup = pyqtSignal(str)
    on_selected = pyqtSignal(IdentityCard)

    def __init__(self, parent, delete_on_close=True):
        super().__init__(parent, Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self.setAttribute(Qt.WA_DeleteOnClose, delete_on_close)
        self._setup_ui()

    def _setup_ui(self):
        self._load(":ui/isni_dialog.ui")
        self._hide_messages()
        self._ok_button.setEnabled(False)

        self._result_container.currentRowChanged.connect(lambda row: self._ok_button.setEnabled(row > -1))
        self._lookup_criteria.textChanged.connect(self._enable_or_disable_lookup_button)
        self._trigger_lookup_action.triggered.connect(lambda: self.on_lookup.emit(self._lookup_criteria.text()))

        self.addAction(self._trigger_lookup_action)
        self.accepted.connect(lambda: self.on_selected.emit(self._selected_identity))

    def lookup_in_progress(self):
        self._progress_indicator.start()
        self._result_container.setDisabled(True)
        self._result_container.setCurrentRow(-1)

    def lookup_successful(self, identities):
        self._progress_indicator.stop()
        self._clear_results()
        self._hide_messages()

        if len(identities) == 0:
            self._no_result_message.setVisible(True)
            return

        self._result_container.setEnabled(True)
        for _, identity in enumerate(identities):
            self._result_container.addItem(self._build_row(identity))

    def lookup_failed(self, _):
        self._progress_indicator.stop()
        self._connection_error_message.setVisible(True)

    def lookup(self, query):
        self.open()
        if query:
            self._lookup_criteria.setText(query)
            self._lookup_button.click()

    @property
    def _selected_identity(self):
        return self._result_container.currentItem().data(Qt.UserRole)

    def _enable_or_disable_lookup_button(self, text):
        self._lookup_button.setEnabled(len(text) > 0)

    @property
    def _ok_button(self):
        return self._dialog_buttons.button(QDialogButtonBox.Ok)

    def _hide_messages(self):
        self._no_result_message.setVisible(False)
        self._connection_error_message.setVisible(False)

    def _build_row(self, identity):
        item = QListWidgetItem(self._build_identity_caption(identity))
        item.setData(Qt.UserRole, identity)
        return item

    def _clear_results(self):
        for index in reversed(range(self._result_container.count())):
            self._result_container.takeItem(index)

    @staticmethod
    def _build_identity_caption(identity):
        label = [identity.full_name]
        if identity.date_of_birth:
            label.append(" (")
            label.append(identity.date_of_birth)
            label.append("-")
            if identity.date_of_death:
                label.append(identity.date_of_death)
            label.append(")")
        label.append(" - ")
        label.append(identity.longest_title)
        return "".join(label)
