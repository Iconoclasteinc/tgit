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

from enum import Enum

from PyQt5.QtWidgets import QHeaderView

from tgit import platforms


class Column:
    def __init__(self, position, resize_mode=QHeaderView.ResizeToContents, mac_width=0, win_width=0):
        self.width = mac_width if platforms.mac else win_width
        self.resize_mode = resize_mode
        self.position = position


class Columns(Enum):
    @classmethod
    def at(cls, col):
        return list(cls.__members__.values())[col]

    @classmethod
    def _values(cls):
        return list([column.value for _, column in cls.__members__.items()])

    @classmethod
    def count(cls):
        return len(cls.__members__)

    @property
    def width(self):
        return self.value.width

    @property
    def resize_mode(self):
        return self.value.resize_mode

    @property
    def position(self):
        return self.value.position
