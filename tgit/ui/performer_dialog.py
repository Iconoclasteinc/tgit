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

from PyQt4.QtCore import Qt, QMargins
from PyQt4.QtGui import QDialog, QFormLayout, QLayout, QPushButton, QDialogButtonBox, QLineEdit, QLabel


class PerformerDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setObjectName('performer-dialog')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(self.tr('Please enter the name of the performer'))
        self.setModal(True)

        self.performer = QLineEdit()
        self.performer.setObjectName('performer')
        self.performer.textChanged.connect(lambda value: self.enableOrDisableOkButton())
        performerLabel = QLabel()
        performerLabel.setText(self.tr('Performer:'))
        self.instrument = QLineEdit()
        self.instrument.setObjectName('instrument')
        self.instrument.textChanged.connect(lambda value: self.enableOrDisableOkButton())
        instrumentLabel = QLabel()
        instrumentLabel.setText(self.tr('Instrument:'))

        layout = QFormLayout()
        layout.addRow(performerLabel, self.performer)
        layout.addRow(instrumentLabel, self.instrument)
        layout.addRow(self.buildButtons())
        layout.setSizeConstraint(QLayout.SetFixedSize)

        self.setLayout(layout)

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

    def getPerformer(self):
        return self.instrument.text(), self.performer.text()

    def enableOrDisableOkButton(self):
        self.okButton.setEnabled(self.formIsFilled())

    def formIsFilled(self):
        return self.instrument.text().strip() != '' and self.performer.text().strip() != ''