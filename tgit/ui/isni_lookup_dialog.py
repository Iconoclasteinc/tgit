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
from PyQt4 import QtGui

from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QDialog, QGridLayout, QDialogButtonBox, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, \
    QRadioButton


class ISNILookupDialog(QDialog):
    lookupISNI = pyqtSignal()

    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.results = None
        self.buttons = None
        self.build()

    def build(self):
        self.setObjectName('isni-lookup-dialog')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)
        resultLayout = QVBoxLayout()
        self.results = QWidget()
        self.results.setLayout(resultLayout)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout = QGridLayout()
        layout.addWidget(self.results, 0, 0, 1, 2)
        layout.addWidget(self.buttons, 1, 0, 1, 2)
        self.setLayout(layout)

    def setIdentities(self, identities):
        layout = self.results.layout()
        self.clearLayout(layout)
        for identity in identities:
            layout.addLayout(self.buildRow(identity))

    def buildRow(self, identity):
        def selectISNI():
            self.selectedIdentity = identity

        isni = QLabel()
        isni.setText(identity[0])

        lastname = QLabel()
        lastname.setText(identity[1])

        firstname = QLabel()
        firstname.setText(identity[2])

        radio = QRadioButton()
        radio.clicked.connect(selectISNI)

        layout = QHBoxLayout()
        layout.addWidget(radio)
        layout.addWidget(isni)
        layout.addWidget(firstname)
        layout.addWidget(lastname)

        return layout

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item, QtGui.QWidgetItem):
                item.widget().close()
            elif isinstance(item, QtGui.QLayoutItem):
                self.clearLayout(item.layout())

            layout.removeItem(item)

    def exec_(self):
        self.lookupISNI.emit()
        return QDialog.exec_(self)