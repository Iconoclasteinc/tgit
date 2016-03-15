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
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QRadioButton

from tgit.ui.helpers.ui_file import UIFile


def make_isni_lookup_dialog(parent, **handlers):
    dialog = ISNILookupDialog(parent)
    for name, handler in handlers.items():
        getattr(dialog, name)(handler)

    return dialog


class ISNILookupDialog(QDialog, UIFile):
    _selected_identity = None

    def __init__(self, parent):
        super().__init__(parent, Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self._setup_ui()

    def _setup_ui(self):
        self._load(":ui/isni_dialog.ui")
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._make_new_functionalities_invisible()

        self._enable_ok_button(enabled=False)
        self._lookup_criteria.textChanged.connect(self._enable_or_disable_lookup_button)

    # noinspection PyUnresolvedReferences
    def on_isni_selected(self, handler):
        self.accepted.connect(lambda: handler(self._selected_identity.id))

    def on_isni_lookup(self, handler):
        def lookup_isni():
            try:
                identities = handler(self._lookup_criteria.text())
                self._clear_results()
                self._display_results(identities)
            except:
                self._display_connection_error()

        self._lookup_button.clicked.connect(lookup_isni)

    def lookup(self, query):
        self.open()
        if query:
            self._lookup_criteria.setText(query)
            self._lookup_button.click()

    def _make_new_functionalities_invisible(self):
        self._result_count.setVisible(False)
        self._assignation_caption.setVisible(False)
        self._assignation_button.setVisible(False)

    def _enable_or_disable_lookup_button(self, text):
        self._lookup_button.setEnabled(len(text) > 0)

    def _enable_ok_button(self, enabled=True):
        self._dialog_buttons.button(QDialogButtonBox.Ok).setEnabled(enabled)

    def _display_results(self, matches):
        if len(matches) == 0:
            self._result_container.addWidget(self._build_no_result_message())

        for index, identity in enumerate(matches):
            self._result_container.addWidget(self._build_row(index, identity))

    def _build_no_result_message(self):
        no_result_label = QLabel()
        no_result_label.setObjectName("_no_result_message")
        no_result_label.setText(self.tr("Your query yielded no result"))
        return no_result_label

    def _display_connection_error(self):
        self._result_container.addWidget(self._build_connection_error_message())

    def _build_connection_error_message(self):
        label = QLabel()
        label.setObjectName("_connection_error_message")
        label.setText(self.tr("Could not connect to the ISNI database. Please retry later."))
        return label

    # noinspection PyUnresolvedReferences
    def _build_row(self, index, identity):
        def select_isni():
            self._enable_ok_button()
            self._selected_identity = identity

        radio = QRadioButton()
        radio.setObjectName("_identity_" + str(index))
        radio.clicked.connect(select_isni)
        radio.setText(self._build_identity_caption(identity))
        return radio

    def _clear_results(self):
        for index in reversed(range(self._result_container.count())):
            if self._result_container.itemAt(index):
                item_widget = self._result_container.takeAt(index).widget()
                item_widget.setParent(None)
                item_widget.close()

    @staticmethod
    def _build_identity_caption(identity):
        label = [identity.full_name]
        if identity.date_of_birth:
            label.append(" (")
            label.append(identity.date_of_birth)
            if identity.date_of_death:
                label.append("-")
                label.append(identity.date_of_death)
            label.append(")")
        label.append(" - ")
        label.append(identity.longest_title)
        text = "".join(label)
        if len(text) > 100:
            text = text[:100] + "..."
        return text
