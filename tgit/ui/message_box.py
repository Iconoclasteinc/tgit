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


def _append_icon_to(message_box, icon_to_append):
    style = message_box.style()
    icon_size = style.pixelMetric(QStyle.PM_MessageBoxIconSize, widget=message_box)
    icon = style.standardIcon(icon_to_append, widget=message_box)
    message_box.setIconPixmap(icon.pixmap(icon_size, icon_size))


def restart_message_box(parent):
    return MessageBox.inform(parent, "You need to restart TGiT for changes to take effect.")


def isni_assignation_failed_message_box(parent, details):
    return MessageBox.warn(parent, "Could not assign an ISNI", details)


def close_album_confirmation_box(parent):
    return ConfirmationBox(parent, "Are you sure you want to stop working on this release?")


class ConfirmationBox(QMessageBox):
    yes = pyqtSignal()

    def __init__(self, parent, message):
        super().__init__(parent)
        self.setObjectName("message_box")
        self.setText(self.tr(message))
        self.setModal(True)
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.buttonClicked.connect(self._button_clicked)
        _append_icon_to(self, QStyle.SP_MessageBoxQuestion)

    def _button_clicked(self, button):
        role = self.buttonRole(button)

        if role == QMessageBox.YesRole:
            self.yes.emit()


class MessageBox(QMessageBox):
    def __init__(self, parent, message, icon=QStyle.SP_MessageBoxInformation, details=None):
        super().__init__(parent)
        self.setObjectName("message_box")
        self.setText(self.tr(message))
        self.setModal(True)
        self.setDetailedText(details)
        self.setStandardButtons(QMessageBox.Ok)
        _append_icon_to(self, icon)

    @staticmethod
    def inform(parent, message, details=None):
        return MessageBox(parent, message, QStyle.SP_MessageBoxInformation, details)

    @staticmethod
    def warn(parent, message, details=None):
        return MessageBox(parent, message, QStyle.SP_MessageBoxWarning, details)

    @staticmethod
    def error(parent, message, details=None):
        return MessageBox(parent, message, QStyle.SP_MessageBoxCritical, details)
