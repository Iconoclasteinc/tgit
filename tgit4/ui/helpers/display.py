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

from PyQt4.QtGui import QApplication, QWidget, QHBoxLayout


def centeredOnScreen(widget):
    show(widget)
    centerOnScreen(widget)
    activate(widget)


def show(widget):
    widget.show()


def centerOnScreen(widget):
    desktop = QApplication.desktop()
    position = widget.frameGeometry()
    position.moveCenter(desktop.availableGeometry().center())
    widget.move(position.topLeft())


def activate(widget):
    from PyQt4.QtCore import QSysInfo

    if hasattr(QSysInfo, 'MacintoshVersion') and QSysInfo.MacintoshVersion > QSysInfo.MV_10_8:
        # Since Maverick, menu bar does not appear until the window is manually activated, so force
        # user to activate by not raising the window
        pass
    else:
        # we can safely raise the window
        widget.raise_()

    widget.activateWindow()


def centeredHorizontally(widget):
    container = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    container.setLayout(layout)
    layout.addStretch()
    layout.addWidget(widget)
    layout.addStretch()
    return container