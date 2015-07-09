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
from collections import namedtuple
from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

from tgit.ui.helpers import formatting


class State(Enum):
    stopped, playing, error = range(3)


class TrackItem:
    state = State.stopped

    def __init__(self, track):
        self.track = track

    @property
    def changed(self):
        return self.track.metadata_changed

    @property
    def is_playing(self):
        return self.state == State.playing

    @property
    def type(self):
        return self.track.type

    @property
    def track_number(self):
        return self.track.track_number

    @property
    def track_title(self):
        return self.track.track_title or ""

    @property
    def lead_performer(self):
        return self.track.lead_performer or ""

    @property
    def release_name(self):
        return self.track.album.release_name or ""

    @property
    def bitrate(self):
        return self.track.bitrate

    @property
    def duration(self):
        return self.track.duration

    def play(self):
        self.state = State.playing

    def stop(self):
        self.state = State.stopped


LEFT_ALIGNED = Qt.AlignLeft | Qt.AlignVCenter
RIGHT_ALIGNED = Qt.AlignRight | Qt.AlignVCenter
RESIZABLE = QHeaderView.Interactive
FIXED = QHeaderView.Fixed
AUTO_ADJUST = QHeaderView.ResizeToContents


Width = namedtuple('Width', ['length', 'resize_mode'])


class CellItem(QTableWidgetItem):
    pass


class Column(Enum):
    class track_number(CellItem):
        width = Width(26, RESIZABLE)

        def __init__(self, track):
            super().__init__(str(track.track_number))
            self.setTextAlignment(RIGHT_ALIGNED)

    class state(CellItem):
        width = Width(24, FIXED)

        def __init__(self, track):
            super().__init__()
            if track.is_playing:
                self.setIcon(QIcon(":/images/volume-up-16.png"))
            self.setTextAlignment(RIGHT_ALIGNED)

    class track_title(CellItem):
        width = Width(300, RESIZABLE)

        def __init__(self, track):
            super().__init__(track.track_title)
            self.setTextAlignment(LEFT_ALIGNED)

    class lead_performer(CellItem):
        width = Width(245, RESIZABLE)

        def __init__(self, track):
            super().__init__(track.lead_performer)
            self.setTextAlignment(LEFT_ALIGNED)

    class release_name(CellItem):
        width = Width(250, RESIZABLE)

        def __init__(self, track):
            super().__init__(track.release_name)
            self.setTextAlignment(LEFT_ALIGNED)

    class bitrate(CellItem):
        width = Width(90, RESIZABLE)

        def __init__(self, track):
            super().__init__("{0} kbps".format(formatting.in_kbps(track.bitrate)))
            self.setTextAlignment(RIGHT_ALIGNED)

    class duration(CellItem):
        width = Width(70, RESIZABLE)

        def __init__(self, track):
            super().__init__(formatting.to_duration(track.duration))
            self.setTextAlignment(RIGHT_ALIGNED)

    @classmethod
    def values(cls):
        return list(cls)

    @classmethod
    def count(cls):
        return len(cls)

    @classmethod
    def at(cls, index):
        return cls.values()[index]

    @property
    def width(self):
        return self.value.width.length

    @property
    def resize_mode(self):
        return self.value.width.resize_mode
