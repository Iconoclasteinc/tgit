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

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QDialog, QLabel, QHBoxLayout, QLayout, QFrame


class ActivityIndicatorDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("activity-indicator-dialog")
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        layout = QHBoxLayout()
        layout.addWidget(build_spinner())
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSizeConstraint(QLayout.SetFixedSize)

        self.setLayout(layout)


def build_spinner():
    movie = QMovie(':/activity-indicator.gif')
    movie.setScaledSize(QSize(75, 75))
    movie.start()
    label = QLabel()
    label.setMovie(movie)
    label.setAlignment(Qt.AlignCenter)

    layout = QHBoxLayout()
    layout.addWidget(label)
    frame = QFrame()
    frame.setObjectName("activity-indicator-dialog-frame")
    frame.setLayout(layout)
    return frame
