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

from PyQt4.QtCore import Qt, pyqtSignal, QFile, QSize, QEventLoop
from PyQt4.QtGui import QDialog, QGridLayout, QDialogButtonBox, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, \
    QRadioButton, QScrollArea, QGroupBox, QFrame, QMovie, QPushButton, QApplication
import time


class ISNILookupDialog(QDialog):
    lookupISNI = pyqtSignal()

    def __init__(self, parent, queue):
        QDialog.__init__(self, parent)
        self.queue = queue
        self.results = None
        self.okButton = None
        self.cancelButton = None
        self.buttons = None
        self.warning = None
        self.noResultLabel = None
        self.loadingMovie = None
        self.loading = None
        self.build()

    def build(self):
        self.setObjectName('isni-lookup-dialog')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)
        self.setWindowTitle(self.tr('ISNI lookup results'))

        self.loadingMovie = QMovie('resources/images/loader_gray_512.gif')
        self.loadingMovie.setScaledSize(QSize(100, 100))
        self.loading = QLabel()
        self.loading.setMovie(self.loadingMovie)
        self.loadingMovie.start()

        self.noResultLabel = QLabel()
        self.noResultLabel.setText(self.tr('Your search yielded no result.'))
        self.noResultLabel.setVisible(False)

        self.results = QFrame()
        self.results.setVisible(False)
        self.results.setFrameStyle(QFrame.StyledPanel)
        self.results.setLayout(QVBoxLayout())

        self.okButton = QPushButton(self.tr('&Ok'))
        self.okButton.setDefault(True)
        self.okButton.setDisabled(True)

        self.cancelButton = QPushButton(self.tr('&Cancel'))

        self.buttons = QDialogButtonBox(Qt.Horizontal)
        self.buttons.setVisible(False)
        self.buttons.addButton(self.okButton, QDialogButtonBox.AcceptRole)
        self.buttons.addButton(self.cancelButton, QDialogButtonBox.RejectRole)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.warning = QLabel()
        self.warning.setVisible(False)
        self.warning.setStyleSheet('color: #F25C0A;')

        layout = QVBoxLayout()
        layout.addWidget(self.loading)
        layout.addWidget(self.warning)
        layout.addWidget(self.results)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    def pollIdentityQueue(self):
        while self.queue.empty():
            QApplication.processEvents(QEventLoop.AllEvents, 50)

        identities = self.queue.get(True)
        self.setIdentities(identities)

    def setIdentities(self, identities):
        numberOfResults, matches = identities

        layout = self.results.layout()
        self.clearLayout(layout)
        for identity in matches:
            layout.addWidget(self.buildRow(identity))

        self.loadingMovie.stop()
        self.loading.setVisible(False)
        self.buttons.setVisible(True)

        if len(matches) > 0:
            self.results.setVisible(True)
        else:
            self.noResultLabel.setVisible(True)

        if int(numberOfResults) > layout.count():
            self.warning.setText(self.tr('Your query returned {numberOfResults} results. If you do not find a match within this list, please refine your search').format(numberOfResults=numberOfResults))
            self.warning.setVisible(True)

    def buildRow(self, identity):
        def selectISNI():
            self.okButton.setEnabled(True)
            self.selectedIdentity = identity

        isni, name = identity
        firstName, lastName = name

        radio = QRadioButton()
        radio.setText('{first} {last}'.format(first=firstName, last=lastName))
        radio.clicked.connect(selectISNI)

        return radio

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item, QtGui.QWidgetItem):
                item.widget().close()
            elif isinstance(item, QtGui.QLayoutItem):
                self.clearLayout(item.layout())

            layout.removeItem(item)
