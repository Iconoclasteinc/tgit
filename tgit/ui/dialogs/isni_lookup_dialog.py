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


def make_isni_lookup_dialog(query, identity_lookup, on_lookup, on_assign, parent=None, delete_on_close=True):
    dialog = ISNILookupDialog(parent, delete_on_close)

    subscriptions = MultiSubscription()
    subscriptions += identity_lookup.on_identities_available.subscribe(in_event_loop(dialog.lookup_successful))
    subscriptions += identity_lookup.on_connection_failed.subscribe(in_event_loop(dialog.connection_failed))
    subscriptions += identity_lookup.on_permission_denied.subscribe(in_event_loop(dialog.permission_denied))
    subscriptions += identity_lookup.on_lookup_start.subscribe(in_event_loop(dialog.lookup_in_progress))
    subscriptions += identity_lookup.on_success.subscribe(in_event_loop(dialog.selection_successful))

    dialog.on_lookup.connect(on_lookup)
    dialog.on_assign.connect(on_assign)
    dialog.on_selected.connect(identity_lookup.identity_selected)
    dialog.finished.connect(lambda accepted: subscriptions.cancel())

    if query:
        dialog.lookup(query)

    return dialog


class ISNILookupDialog(QDialog, UIFile):
    on_lookup = pyqtSignal(str)
    on_assign = pyqtSignal()
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
        self._ok_button.clicked.connect(lambda: self.on_selected.emit(self._selected_identity))
        self._assignation_button.clicked.connect(self.on_assign.emit)

        self.addAction(self._trigger_lookup_action)

    def lookup_in_progress(self):
        self._progress_indicator.start()
        self._result_container.setDisabled(True)
        self._result_container.setCurrentRow(-1)

    def lookup_successful(self, identities):
        self._progress_indicator.stop()
        self._clear_results()
        self._hide_messages()

        if len(identities) == 0:
            self._show_no_result_message()
            self._assignation_button.setEnabled(True)
            return

        self._assignation_button.setEnabled(False)
        self._result_container.setEnabled(True)
        for _, identity in enumerate(identities):
            self._result_container.addItem(self._build_row(identity))

        if identities.overflows():
            self._show_refine_search_result_message(identities.total_count)

    def selection_successful(self):
        self.accept()

    def _show_no_result_message(self):
        self._result_message.setVisible(True)
        self._result_message.setText(self.tr("Your query yielded no result."))

    def _show_refine_search_result_message(self, total_count):
        self._result_message.setVisible(True)
        self._result_message.setText(
            self.tr("Your search yielded {} results. Please refine your search.").format(total_count))

    def connection_failed(self):
        self._progress_indicator.stop()
        self._connection_error_message.setVisible(True)

    def permission_denied(self):
        self._progress_indicator.stop()
        self._permission_denied_message.setVisible(True)

    def lookup(self, query):
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
        self._result_message.setVisible(False)
        self._connection_error_message.setVisible(False)
        self._permission_denied_message.setVisible(False)

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
