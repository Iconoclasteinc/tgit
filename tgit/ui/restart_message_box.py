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
from PyQt5.QtCore import pyqtSignal

from PyQt5.QtWidgets import QMessageBox, QStyle


def _create_message_box(parent, message, details=None):
    message_box = QMessageBox(parent)
    message_box.setObjectName("message_box")
    message_box.setText(message_box.tr(message))
    if details is not None:
        message_box.setDetailedText(details)
    message_box.setModal(True)
    return message_box


def _append_icon_to(message_box, icon_to_append):
    style = message_box.style()
    icon_size = style.pixelMetric(QStyle.PM_MessageBoxIconSize, widget=message_box)
    icon = style.standardIcon(icon_to_append, widget=message_box)
    message_box.setIconPixmap(icon.pixmap(icon_size, icon_size))


def isni_assignation_failed_message_box(parent, details):
    message_box = _create_message_box(parent, "Could not assign an ISNI", details)
    _append_icon_to(message_box, QStyle.SP_MessageBoxWarning)

    return message_box


def close_album_confirmation_box(parent):
    message_box = ConfirmationBox(parent, "???")
    _append_icon_to(message_box, QStyle.SP_MessageBoxQuestion)
    return message_box


class ConfirmationBox(QMessageBox):
    yes = pyqtSignal()

    def __init__(self, parent, message):
        super().__init__(parent)
        self.setObjectName("message_box")
        self.setText(self.tr(message))
        self.setModal(True)
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.buttonClicked.connect(self._button_clicked)

    def _button_clicked(self, button):
        role = self.buttonRole(button)

        if role == QMessageBox.YesRole:
            self.yes.emit()


class RestartMessageBox(QMessageBox):
    def __init__(self, parent=None):
        QMessageBox.__init__(self, parent)
        self.setObjectName("restart-message")
        self.setText(self.tr("You need to restart TGiT for changes to take effect."))

    def display(self):
        self.open()