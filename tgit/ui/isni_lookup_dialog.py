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
        numberOfResults = '0'
        matches = []

        if not self.connectionError:
            numberOfResults, matches = identities

        self.parent = parent
        self.okButton = None
        self.selectedIdentity = None
        self.build(int(numberOfResults), matches)

    def build(self, numberOfResults, matches):
        self.setObjectName('isni-lookup-dialog')
        self.setWindowFlags(Qt.Dialog)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(self.tr('Please select from the list of identities'))
        self.setModal(True)

        layout = QVBoxLayout()
        layout.addWidget(self.buildResults(matches, numberOfResults))
        layout.addWidget(self.buildButtons())
        layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(layout)

    def buildResults(self, matches, numberOfResults):
        resultsLayout = QVBoxLayout()
        results = QGroupBox()
        results.setObjectName('lookup-results')
        results.setLayout(resultsLayout)

        if self.connectionError:
            resultsLayout.addWidget(self.buildConnectionErrorMessage())
            return results

        if len(matches) < int(numberOfResults):
            resultsLayout.addWidget(self.buildWarning())
        if len(matches) == 0:
            resultsLayout.addWidget(self.buildNoResultMessage())
        for identity in matches:
            resultsLayout.addWidget(self.buildRow(identity))
        return results

    def buildButtons(self):
        self.okButton = QPushButton(self.tr('&OK'))
        self.okButton.setObjectName('ok-button')
        self.okButton.setDefault(True)
        self.okButton.setDisabled(True)
        cancelButton = QPushButton(self.tr('&Cancel'))
        cancelButton.setObjectName('cancel-button')
        cancelButton.setEnabled(True)
        buttons = QDialogButtonBox(Qt.Horizontal)
        buttons.setObjectName('action-buttons')
        buttons.addButton(self.okButton, QDialogButtonBox.AcceptRole)
        buttons.addButton(cancelButton, QDialogButtonBox.RejectRole)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.setContentsMargins(QMargins(0, 0, 7, 0))
        return buttons

    def buildWarning(self):
        warning = QLabel()
        warning.setObjectName('results-exceeds-shown')
        warning.setText(self.tr('If you do not find a match within this list, please refine your search'
                                ' (only the first 20 results are shown)'))
        return warning

    def buildNoResultMessage(self):
        noResultLabel = QLabel()
        noResultLabel.setObjectName('no-result-message')
        noResultLabel.setText(self.tr('Your query yielded no result'))
        return noResultLabel

    def buildConnectionErrorMessage(self):
        label = QLabel()
        label.setObjectName('connection-error-message')
        label.setText(self.tr('Could not connect to the ISNI database. Please retry later.'))
        return label

    def buildRow(self, identity):
        def selectISNI():
            self.okButton.setEnabled(True)
            self.selectedIdentity = identity

        radio = QRadioButton()
        radio.clicked.connect(selectISNI)
        radio.setText(self.buildIdentityCaption(identity))
        return radio

    def buildIdentityCaption(self, identity):
        _, personalInformations = identity
        name, date, title = personalInformations

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
