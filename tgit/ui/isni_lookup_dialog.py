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


class ISNILookupDialog(QDialog):
    def __init__(self, parent, identities):
        super().__init__(parent)
        self.connectionError = type(identities) is requests.exceptions.ConnectionError
        number_of_results = '0'
        matches = []

        if not self.connectionError:
            number_of_results, matches = identities

        self.okButton = None
        self.selectedIdentity = None
        self._build(int(number_of_results), matches)

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

    def _build_results(self, matches, number_of_results):
        results_layout = QVBoxLayout()
        results = QGroupBox()
        results.setObjectName("lookup-results")
        results.setLayout(results_layout)

        if self.connectionError:
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
        self.okButton = QPushButton(self.tr('&OK'))
        self.okButton.setObjectName("ok-button")
        self.okButton.setDefault(True)
        self.okButton.setDisabled(True)
        cancel_button = QPushButton(self.tr('&Cancel'))
        cancel_button.setObjectName("cancel-button")
        cancel_button.setEnabled(True)
        buttons = QDialogButtonBox(Qt.Horizontal)
        buttons.setObjectName("action-buttons")
        buttons.addButton(self.okButton, QDialogButtonBox.AcceptRole)
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
            self.okButton.setEnabled(True)
            self.selectedIdentity = identity

        radio = QRadioButton()
        radio.setObjectName("identity_radio_" + str(index))
        radio.clicked.connect(select_isni)
        radio.setText(self.build_identity_caption(identity))
        return radio

    def build_identity_caption(self, identity):
        _, personal_informations = identity
        name, date, title = personal_informations

        label = [name]
        if date != '':
            label.append(' (')
            label.append(date)
            label.append(')')
        label.append(' - ')
        label.append(title)
        text = ''.join(label)
        if len(text) > 100:
            text = text[:100] + '...'
        return text
