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
from PyQt5 import QtGui

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLayout, QPushButton, QDialogButtonBox, QLineEdit, QLabel, QHBoxLayout, \
    QSpacerItem, QWidget, QVBoxLayout, QGroupBox, QWidgetItem


class PerformerDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setObjectName('performer-dialog')
        self.setWindowFlags(Qt.Dialog)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(self.tr('Please enter the name of the performer'))
        self.setModal(True)

        self.uniqueIdentifier = 0
        self.performersTable = self.buildPerformerTable()

        boxLayout = QVBoxLayout()
        boxLayout.addWidget(self.buildHeader())
        boxLayout.addWidget(self.performersTable)
        boxLayout.addWidget(self.buildAddRowButton())

        box = QGroupBox()
        box.setObjectName('form-box')
        box.setLayout(boxLayout)

        layout = QVBoxLayout()
        layout.addWidget(box)
        layout.addWidget(self.buildButtons())
        layout.setSizeConstraint(QLayout.SetFixedSize)

        self.setLayout(layout)

    def buildHeader(self):
        performerLabel = QLabel()
        performerLabel.setText(self.tr('Performer:'))

        instrumentLabel = QLabel()
        instrumentLabel.setText(self.tr('Instrument:'))

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(instrumentLabel)
        layout.addWidget(performerLabel)
        layout.addItem(QSpacerItem(35, 0))

        widget = QWidget()
        widget.setObjectName('performers-table-header')
        widget.setLayout(layout)
        return widget

    def buildAddRowButton(self):
        button = QPushButton()
        button.setObjectName('add-performer')
        button.setText(self.tr('ADD A PERFORMER'))
        button.clicked.connect(
            lambda: self.performersTable.layout().addWidget(self.buildPerformerRow()))
        return button

    def display(self, performers):
        layout = self.performersTable.layout()
        if performers:
            for index, performer in enumerate(performers):
                layout.addWidget(self.buildPerformerRow(performer))
        else:
            layout.addWidget(self.buildPerformerRow())

    def buildPerformerTable(self):
        widget = QWidget()
        widget.setObjectName('performers-table')
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        return widget

    def buildPerformerRow(self, performer=None):
        index = self.uniqueIdentifier
        self.uniqueIdentifier += 1

        instrument = name = None
        if performer is not None:
            instrument, name = performer

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.buildLineEdit('instrument-%(index)i' % locals(), instrument))
        layout.addWidget(self.buildLineEdit('performer-%(index)i' % locals(), name))

        if index == 0:
            layout.addItem(QSpacerItem(self.getSpacerWidth(), 0))
        else:
            layout.addWidget(self.buildRemoveLineButton('remove-performer-%(index)i' % locals()))

        widget = QWidget()
        widget.setObjectName('performers-row-%(index)i' % locals())
        widget.setLayout(layout)
        return widget

    def buildRemoveLineButton(self, name):
        button = QPushButton()
        button.setObjectName(name)
        button.setText('-')
        button.clicked.connect(lambda: self.removeRowContaining(button.objectName()))
        button.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        return button

    def buildButtons(self):
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.setObjectName('action-buttons')
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.setContentsMargins(0, 0, 7, 0)
        return buttons

    def buildLineEdit(self, name, text=None):
        edit = QLineEdit()
        edit.setObjectName(name)
        edit.setText(text)
        return edit

    def getPerformers(self):
        performers = []
        for i in range(self.performersTable.layout().count()):
            performer = self.getPerformerFrom(self.performersTable.layout().itemAt(i).widget().layout())
            if performer is not None:
                performers.append(performer)
        return performers

    def getPerformerFrom(self, rowLayout):
        instrument = rowLayout.itemAt(0).widget().text()
        name = rowLayout.itemAt(1).widget().text()

        if instrument.strip() != '' and name.strip() != '':
            return instrument, name
        return None

    def removeRowContaining(self, buttonName):
        row = self.findRowContaining(buttonName)
        if row:
            self.removeRow(row)

    def findRowContaining(self, buttonName):
        for i in range(self.performersTable.layout().count()):
            rowLayout = self.findWidgetInRow(self.performersTable.layout().itemAt(i).widget(), buttonName)
            if rowLayout:
                return rowLayout
        return None

    def findWidgetInRow(self, row, buttonName):
        layout = row.layout()
        for j in range(layout.count()):
            item = layout.itemAt(j)
            if isinstance(item, QWidgetItem) and item.widget().objectName() == buttonName:
                return row
        return None

    def removeRow(self, row):
        layout = row.layout()
        for k in reversed(range(layout.count())):
            layout.itemAt(k).widget().close()
        row.close()
        self.performersTable.layout().removeWidget(row)

    def getSpacerWidth(self):
        spacerSize = 34
        MAC = hasattr(QtGui, "qt_mac_set_native_menubar")
        if MAC:
            spacerSize = 39

        return spacerSize