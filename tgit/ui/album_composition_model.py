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

from PyQt5.QtCore import QObject, QAbstractTableModel, QModelIndex, Qt, pyqtSignal

from tgit.album import AlbumListener
from tgit.audio import PlayerListener
from tgit.ui.helpers import formatting


# We need to keep Row until we get rid of the playing state
class Row(QObject, AlbumListener, PlayerListener):
    rowChanged = pyqtSignal(object)

    # todo remove album from params
    def __init__(self, album, track, playing=False):
        QObject.__init__(self)
        self.album = album
        self.track = track
        self.inPlay = playing

    @property
    def trackTitle(self):
        return self.track.track_title

    def leadPerformer(self):
        return self.track.lead_performer

    def releaseName(self):
        return self.album.release_name

    def bitrate(self):
        return self.track.bitrate

    def duration(self):
        return self.track.duration

    @property
    def playback_supported(self):
        return self.track.filename.endswith('.mp3')

    def track_state_changed(self, track):
        self.signalRowChange()

    def albumStateChanged(self, album):
        self.signalRowChange()

    def loading(self, filename):
        if filename == self.track.filename:
            self.inPlay = True
            self.signalRowChange()

    def paused(self, filename):
        self.stopped(filename)

    def stopped(self, filename):
        if filename == self.track.filename:
            self.inPlay = False
            self.signalRowChange()

    def signalRowChange(self):
        self.rowChanged.emit(self)


class Column(QObject):
    def __init__(self, name, value):
        QObject.__init__(self)
        self._name = name
        self.value = value

    @property
    def name(self):
        return self.tr(self._name)


class ColumnEnum(type):
    def __len__(cls):
        return len(cls.__values__)

    def index(cls, column):
        return cls.__values__.index(column)

    def __getitem__(cls, item):
        return cls.__values__[item]


class Columns(metaclass=ColumnEnum):
    trackTitle = Column(name='Track Title', value=lambda row: row.trackTitle)
    leadPerformer = Column(name='Lead Performer', value=Row.leadPerformer)
    releaseName = Column(name="Release Name", value=Row.releaseName)
    bitrate = Column(name='Bitrate', value=lambda row: '%s kbps' % formatting.inKbps(row.bitrate()))
    duration = Column(name='Duration', value=lambda row: formatting.toDuration(row.duration()))
    play = Column(name='', value=lambda row: (row.inPlay, row.playback_supported))

    __values__ = trackTitle, leadPerformer, releaseName, bitrate, duration, play


class AlbumCompositionModel(QAbstractTableModel, AlbumListener):
    def __init__(self, album, player, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.album = album
        self.album.addAlbumListener(self)
        self.player = player
        self.rows = []

    @property
    def tracks(self):
        return tuple(self.rows)

    def columnCount(self, index=QModelIndex()):
        return len(Columns)

    def rowCount(self, parent=QModelIndex()):
        return len(self.rows)

    def flags(self, index):
        return Qt.ItemFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if not role == Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return Columns[section].name
        else:
            return str(section + 1)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.album)):
            return None

        if role != Qt.DisplayRole:
            return None

        return Columns[index.column()].value(self.rows[index.row()])

    def trackAt(self, position):
        return self.rows[position].track

    def albumStateChanged(self, album):
        self.dataChanged.emit(self.index(0, Columns.index(Columns.releaseName)),
                              self.index(self.rowCount() - 1, Columns.index(Columns.releaseName)))

    def trackAdded(self, track, position):
        row = Row(self.album, track, self.player.is_playing(track.filename))
        track.metadata_changed.subscribe(row.track_state_changed)
        self.album.addAlbumListener(row)
        self.player.add_player_listener(row)
        self.rows.insert(position, row)
        row.rowChanged.connect(self.rowChanged)
        self.insertRows(position, 1, QModelIndex())

    def rowChanged(self, row):
        position = self.rows.index(row)
        self.dataChanged.emit(self.index(position, 0), self.index(position, len(Columns) - 1))

    def trackRemoved(self, track, position):
        row = self.rows[position]
        track.metadata_changed.unsubscribe(row.track_state_changed)
        self.album.removeAlbumListener(row)
        self.player.remove_player_listener(row)
        row.rowChanged.disconnect()
        self.rows.remove(row)
        self.removeRows(position, 1, QModelIndex())

    def insertRows(self, position, rows, parent):
        self.beginInsertRows(parent, position, position + rows - 1)
        self.endInsertRows()

    def removeRows(self, position, rows, parent):
        self.beginRemoveRows(parent, position, position + rows - 1)
        self.endRemoveRows()