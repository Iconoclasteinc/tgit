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

from PyQt4.QtCore import Qt, pyqtSignal, QFile, QSize, QEventLoop, QMargins
from PyQt4.QtGui import QDialog, QGridLayout, QDialogButtonBox, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, \
    QRadioButton, QScrollArea, QGroupBox, QFrame, QMovie, QPushButton, QApplication, QLayout, QSizePolicy
import time


class ISNILookupDialog(QDialog):
    lookupISNI = pyqtSignal()

    def __init__(self, parent, queryExpression, queue):
        QDialog.__init__(self, parent)
        self.queue = queue
        self.okButton = None
        self.cancelButton = None
        self.results = None
        self.queryExpression = queryExpression
        self.parent = parent
        self.build()

    def title(self):
        return (self.tr('ISNI lookup for ') + self.queryExpression).upper()

    def center(self):
        QApplication.processEvents(QEventLoop.AllEvents)
        point = self.parent.mapToGlobal(self.parent.rect().center())
        self.move(point.x() - self.width() / 2, point.y() - self.height() / 2)

    def buildSpinner(self):
        loadingMovie = QMovie('resources/images/loader_gray_512.gif')
        loadingMovie.setScaledSize(QSize(75, 75))
        loadingMovie.start()
        loadingLabel = QLabel()
        loadingLabel.setMovie(loadingMovie)
        loadingLabel.setAlignment(Qt.AlignCenter)
        return loadingLabel

    def build(self):
        self.setObjectName('isni-lookup-dialog')
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.results = QGroupBox(self.title())
        self.results.setObjectName('lookup-results')
        self.results.setLayout(QVBoxLayout())
        self.results.layout().addWidget(self.buildSpinner())

        self.okButton = QPushButton(self.tr('&OK'))
        self.okButton.setObjectName('ok-button')
        self.okButton.setDefault(True)
        self.okButton.setDisabled(True)
        self.cancelButton = QPushButton(self.tr('&Cancel'))
        self.cancelButton.setObjectName('cancel-button')
        self.cancelButton.setDisabled(True)
        buttons = QDialogButtonBox(Qt.Horizontal)
        buttons.setObjectName('action-buttons')
        buttons.addButton(self.okButton, QDialogButtonBox.AcceptRole)
        buttons.addButton(self.cancelButton, QDialogButtonBox.RejectRole)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.setContentsMargins(QMargins(0, 0, 7, 0))

        layout = QVBoxLayout()
        layout.addWidget(self.results)
        layout.addWidget(buttons)
        layout.setSizeConstraint(QLayout.SetFixedSize)

        self.setLayout(layout)

    def pollIdentityQueue(self):
        while self.queue.empty():
            QApplication.processEvents(QEventLoop.AllEvents, 100)

        identities = self.queue.get(True)
        self.setIdentities(identities)

    def setIdentities(self, identities):
        numberOfResults, matches = identities

        layout = self.results.layout()
        layout.takeAt(0).widget().close()
        if len(matches) < int(numberOfResults):
            layout.addWidget(self.buildWarning())

        if len(matches) == 0:
            layout.addWidget(self.buildNoResultMessage())

        for identity in matches:
            layout.addWidget(self.buildRow(identity))

        self.cancelButton.setEnabled(True)
        self.center()

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
        firstName, lastName, date, title = personalInformations

        label = [firstName, ' ', lastName]
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
