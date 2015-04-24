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

from PyQt5.QtWidgets import QMessageBox, QStyle
from tgit.isni.name_registry import NameRegistry


def _get_details_prefix_from(code):
    if code == NameRegistry.Codes.INVALID_DATA:
        return "Invalid data:"
    elif code == NameRegistry.Codes.INVALID_FORMAT:
        return "Invalid format:"
    elif code == NameRegistry.Codes.SPARSE:
        return "Sparse data:"
    return ""


def _create_message_box(parent, message, details=None):
    message_box = QMessageBox(parent)
    message_box.setObjectName("message_box")
    message_box.setText(message_box.tr(message))
    if details is not None:
        message_box.setDetailedText(details)
    message_box.setModal(True)
    return message_box


def _append_warning_icon_to(message_box):
    style = message_box.style()
    icon_size = style.pixelMetric(QStyle.PM_MessageBoxIconSize, widget=message_box)
    icon = style.standardIcon(QStyle.SP_MessageBoxWarning, widget=message_box)
    message_box.setIconPixmap(icon.pixmap(icon_size, icon_size))


def isni_assignation_failed_message_box(parent, code, details):
    prefix = _get_details_prefix_from(code)
    message_box = _create_message_box(parent, "Could not assign an ISNI", "{0} {1}".format(prefix, details))
    _append_warning_icon_to(message_box)

    return message_box


class RestartMessageBox(QMessageBox):
    def __init__(self, parent=None):
        QMessageBox.__init__(self, parent)
        self.setObjectName('restart-message')
        self.setText(self.tr("You need to restart TGiT for changes to take effect."))

    def display(self):
        self.open()