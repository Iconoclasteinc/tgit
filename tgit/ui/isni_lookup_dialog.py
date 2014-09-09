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

    def __init__(self, parent, queryExpression, queue):
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
        self.queryExpression = queryExpression
        self.build()

    def build(self):
        self.setObjectName('isni-lookup-dialog')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)
        self.setWindowTitle(self.tr('ISNI lookup for ') + self.queryExpression)

        self.loadingMovie = QMovie('resources/images/loader_gray_512.gif')
        self.loadingMovie.setScaledSize(QSize(75, 75))
        self.loading = QLabel()
        self.loading.setMovie(self.loadingMovie)
        self.loadingMovie.start()

        self.noResultLabel = QLabel()
        self.noResultLabel.setObjectName('no-result-message')
        self.noResultLabel.setText(self.tr('Your query yielded no result.'))
        self.noResultLabel.setVisible(False)

        self.results = QGroupBox(self.tr('ISNI lookup for ') + self.queryExpression)
        self.results.setObjectName('lookup-results')
        self.results.setVisible(False)
        self.results.setLayout(QVBoxLayout())

        self.okButton = QPushButton(self.tr('&OK'))
        self.okButton.setObjectName('ok-button')
        self.okButton.setDefault(True)
        self.okButton.setDisabled(True)

        self.cancelButton = QPushButton(self.tr('&Cancel'))
        self.cancelButton.setObjectName('cancel-button')

        self.buttons = QDialogButtonBox(Qt.Horizontal)
        self.buttons.setObjectName('action-buttons')
        self.buttons.setVisible(False)
        self.buttons.addButton(self.okButton, QDialogButtonBox.AcceptRole)
        self.buttons.addButton(self.cancelButton, QDialogButtonBox.RejectRole)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.warning = QLabel()
        self.warning.setObjectName('results-exceeds-shown')
        self.warning.setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(self.loading)
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

        if int(numberOfResults) > layout.count():
            layout.addWidget(self.warning)
            self.warning.setText(self.tr('Your query returned {numberOfResults} results. Only the first 20 results are '
                                         'shown.\nIf you do not find a match within this list, please refine your '
                                         'search').format(numberOfResults=numberOfResults))
            self.warning.setVisible(True)

        if layout.count() == 0:
            layout.addWidget(self.noResultLabel)
            self.noResultLabel.setVisible(True)

        for identity in matches:
            layout.addWidget(self.buildRow(identity))

        self.loadingMovie.stop()
        self.loading.setVisible(False)
        self.buttons.setVisible(True)
        self.results.setVisible(True)

    def buildRow(self, identity):
        def selectISNI():
            self.okButton.setEnabled(True)
            self.selectedIdentity = identity

        isni, personalInformations = identity
        firstName, lastName, date, title = personalInformations

        label = [firstName, ' ', lastName]
        if date != '':
            label.append(' (')
            label.append(date)
            label.append(')')

        label.append(' - ')
        if len(title) > 75:
            label.append(title[:75])
            label.append('...')
        else:
            label.append(title)

        radio = QRadioButton()
        radio.setText(''.join(label))
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
