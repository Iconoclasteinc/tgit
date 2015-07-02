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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QStyle


class MessageBoxes:
    parent = None

    def show_error(self, message, details=None):
        message_box = MessageBox.error(self.parent, message, details)
        message_box.open()
        return message_box

    def inform_restart_required(self):
        message_box = MessageBox.inform(self.parent, "You need to restart TGiT for changes to take effect.")
        message_box.open()
        return message_box

    def warn_isni_assignation_failed(self, details=None):
        message_box = MessageBox.warn(self.parent, "Could not assign an ISNI", details)
        message_box.open()
        return message_box

    def confirm_close_album(self, **handlers):
        message_box = ConfirmationBox(self.parent, "Are you sure you want to stop working on this release?", **handlers)
        message_box.open()
        return message_box

    def confirm_album_overwrite(self, **handlers):
        message_box = ConfirmationBox(self.parent, "This album already exists. Are you sure you want to replace it?", **handlers)
        message_box.open()
        return message_box


def _append_icon_to(message_box, icon_to_append):
    style = message_box.style()
    icon_size = style.pixelMetric(QStyle.PM_MessageBoxIconSize, widget=message_box)
    icon = style.standardIcon(icon_to_append, widget=message_box)
    message_box.setIconPixmap(icon.pixmap(icon_size, icon_size))


class ConfirmationBox(QMessageBox):
    _on_accept = lambda: None

    def __init__(self, parent, message, **handlers):
        super().__init__(parent)

        self.setObjectName("message_box")
        self.setText(self.tr(message))
        self.setModal(True)
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.buttonClicked.connect(self._button_clicked)
        _append_icon_to(self, QStyle.SP_MessageBoxQuestion)

        for name, handler in handlers.items():
            getattr(self, name)(handler)

    def _button_clicked(self, button):
        role = self.buttonRole(button)

        if role == QMessageBox.YesRole:
            self._on_accept()

    def on_accept(self, on_accept):
        self._on_accept = on_accept


class MessageBox(QMessageBox):
    def __init__(self, parent, message, icon=QStyle.SP_MessageBoxInformation, details=None):
        super().__init__(parent)
        self.setObjectName("message_box")
        self.setText(self.tr(message))
        self.setModal(True)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
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
