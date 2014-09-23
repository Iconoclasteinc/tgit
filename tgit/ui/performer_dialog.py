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
from PyQt4.QtGui import QDialog, QFormLayout, QLayout, QPushButton, QDialogButtonBox, QLineEdit, QLabel, QHBoxLayout
from PyQt4.QtGui import QVBoxLayout, QGroupBox


class PerformerDialog(QDialog):
    def __init__(self, parent=None, performers=None):
        QDialog.__init__(self, parent)
        self.setObjectName('performer-dialog')
        self.setWindowFlags(Qt.Dialog)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(self.tr('Please enter the name of the performer'))
        self.setModal(True)

        self.rowsLayout = self.buildPerformerRows(performers)
        formLayout = QVBoxLayout()
        formLayout.addLayout(self.buildHeader())
        formLayout.addLayout(self.rowsLayout)
        formLayout.addWidget(self.buildAddRowButton())

        formBox = QGroupBox()
        formBox.setObjectName('form-box')
        formBox.setLayout(formLayout)

        layout = QVBoxLayout()
        layout.addWidget(formBox)
        layout.addWidget(self.buildButtons())
        layout.setSizeConstraint(QLayout.SetFixedSize)

        self.setLayout(layout)

    def buildHeader(self):
        performerLabel = QLabel()
        performerLabel.setText(self.tr('Performer:'))

        instrumentLabel = QLabel()
        instrumentLabel.setText(self.tr('Instrument:'))

        layout = QHBoxLayout()
        layout.addWidget(performerLabel)
        layout.addWidget(instrumentLabel)
        return layout

    def buildAddRowButton(self):
        addRowButton = QPushButton()
        addRowButton.setObjectName('add-performer')
        addRowButton.setText(self.tr('ADD A PERFORMER'))
        addRowButton.clicked.connect(lambda: self.rowsLayout.addLayout(self.buildPerformerRow(index=self.rowsLayout.count())))
        return addRowButton

    def buildPerformerRows(self, performers):
        layout = QVBoxLayout()
        if performers is not None:
            for index, performer in enumerate(performers):
                layout.addLayout(self.buildPerformerRow(performer, index))
        else:
            layout.addLayout(self.buildPerformerRow(index=0))

        return layout

    def buildPerformerRow(self, performer=None, index=None):
        instrument = name = None
        if performer is not None:
            instrument, name = performer

        layout = QHBoxLayout()
        layout.addWidget(self.buildLineEdit('instrument-%(index)i' % locals(), instrument))
        layout.addWidget(self.buildLineEdit('performer-%(index)i' % locals(), name))
        return layout

    def buildButtons(self):
        self.okButton = QPushButton(self.tr('&OK'))
        self.okButton.setObjectName('ok-button')
        self.okButton.setDefault(True)
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

    def buildLineEdit(self, name, text=None):
        edit = QLineEdit()
        edit.setObjectName(name)
        edit.setText(text)
        return edit

    def getPerformers(self):
        performers = []
        index = 0
        while index < self.rowsLayout.count():
            performer = self.getPerformerFrom(self.rowsLayout.itemAt(index).layout())
            if performer is not None:
                performers.append(performer)
            index += 1
        return performers

    def getPerformerFrom(self, rowLayout):
        instrument = rowLayout.itemAt(0).widget().text()
        name = rowLayout.itemAt(1).widget().text()

        if instrument.strip() != '' and name.strip() != '':
            return instrument, name
        return None