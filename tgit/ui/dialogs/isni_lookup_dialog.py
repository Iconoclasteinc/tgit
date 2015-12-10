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

from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QRadioButton, QGroupBox, QPushButton, \
    QLayout
import requests


def make_isni_lookup_dialog(parent, identities, **handlers):
    dialog = ISNILookupDialog(parent, identities)
    for name, handler in handlers.items():
        getattr(dialog, name)(handler)

    dialog.open()
    return dialog


STYLESHEET = """
    QGroupBox {
        border: 1px solid #DDDDDD;
        border-bottom: 2px solid rgba(0, 0, 0, 20%);
        background-color: white;
        padding: 17px 14px 14px 0px;
        margin: 5px 8px;
        font-size: 10px;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 1px;
        padding: 0 3px;
        color: #777777;
        border: 1px solid #DFDFDF;
        background-color: #F7F7F7;
    }

    QRadioButton::indicator {
        width: 22px;
        height: 22px;
    }

    QRadioButton::indicator::unchecked {
        image: url(:/images/radio-unchecked.png);
    }

    QRadioButton::indicator:unchecked:focus {
        image: url(:/images/radio-unchecked-focus.png);
    }

    QRadioButton::indicator:unchecked:pressed {
        image: url(:/images/radio-unchecked-pressed.png)
    }

    QRadioButton::indicator::checked {
        image: url(:/images/radio-checked.png)
    }

    QRadioButton::indicator:checked:focus {
        image: url(:/images/radio-checked-focus.png)
    }

    QRadioButton::indicator:checked:pressed {
        image: url(:/images/radio-checked-pressed.png)
    }
"""


class ISNILookupDialog(QDialog):
    def __init__(self, parent, identities):
        super().__init__(parent)
        self.ok_button = None
        self.selected_identity = None

        self.connection_error = type(identities) is requests.ConnectionError
        matches = identities if not self.connection_error else []
        self._build(len(matches), matches)

    def on_isni_selected(self, handler):
        self.accepted.connect(lambda: handler(self.selected_identity))

    def _build(self, number_of_results, matches):
        self.setObjectName("isni-lookup-dialog")
        self.setWindowFlags(Qt.Dialog)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(self.tr("Please select from the list of identities"))
        self.setModal(True)

        layout = QVBoxLayout()
        layout.addWidget(self._build_results(matches, number_of_results))
        layout.addWidget(self._build_buttons())
        layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(layout)

        self.setStyleSheet(STYLESHEET)

    def _build_results(self, matches, number_of_results):
        results_layout = QVBoxLayout()
        results = QGroupBox()
        results.setObjectName("lookup-results")
        results.setLayout(results_layout)

        if self.connection_error:
            results_layout.addWidget(self._build_connection_error_message())
            return results

        if len(matches) < int(number_of_results):
            results_layout.addWidget(self._build_warning())
        if len(matches) == 0:
            results_layout.addWidget(self._build_no_result_message())
        for index, identity in enumerate(matches):
            results_layout.addWidget(self._build_row(index, identity))
        return results

    def _build_buttons(self):
        self.ok_button = QPushButton(self.tr("&OK"))
        self.ok_button.setObjectName("ok-button")
        self.ok_button.setDefault(True)
        self.ok_button.setDisabled(True)
        cancel_button = QPushButton(self.tr("&Cancel"))
        cancel_button.setObjectName("cancel-button")
        cancel_button.setEnabled(True)
        buttons = QDialogButtonBox(Qt.Horizontal)
        buttons.setObjectName("action-buttons")
        buttons.addButton(self.ok_button, QDialogButtonBox.AcceptRole)
        buttons.addButton(cancel_button, QDialogButtonBox.RejectRole)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.setContentsMargins(QMargins(0, 0, 7, 0))
        return buttons

    def _build_warning(self):
        warning = QLabel()
        warning.setObjectName("results-exceeds-shown")
        warning.setText(self.tr("If you do not find a match within this list, please refine your search"
                                " (only the first 20 results are shown)"))
        return warning

    def _build_no_result_message(self):
        no_result_label = QLabel()
        no_result_label.setObjectName("no-result-message")
        no_result_label.setText(self.tr("Your query yielded no result"))
        return no_result_label

    def _build_connection_error_message(self):
        label = QLabel()
        label.setObjectName("connection-error-message")
        label.setText(self.tr("Could not connect to the ISNI database. Please retry later."))
        return label

    def _build_row(self, index, identity):
        def select_isni():
            self.ok_button.setEnabled(True)
            self.selected_identity = identity

        radio = QRadioButton()
        radio.setObjectName("identity_radio_" + str(index))
        radio.clicked.connect(select_isni)
        radio.setText(self._build_identity_caption(identity))
        return radio

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
