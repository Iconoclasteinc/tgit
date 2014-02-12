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

from PyQt4.QtCore import QObject, QAbstractTableModel, QModelIndex, Qt, pyqtSignal

from tgit.album import AlbumListener
from tgit.track import TrackListener
from tgit.audio.player import PlayerListener
from tgit.ui import display


class Row(QObject, TrackListener, PlayerListener):
    rowChanged = pyqtSignal(object)

    def __init__(self, album, track, playing=False):
        super(Row, self).__init__()
        self._album = album
        self._track = track
        self._playing = playing

    @property
    def trackTitle(self):
        return self._track.trackTitle

    def leadPerformer(self):
        return self._album.leadPerformer

    def releaseName(self):
        return self._album.releaseName

    def bitrate(self):
        return self._track.bitrate

    def duration(self):
        return self._track.duration

    def playing(self):
        # We cannot just rely on the player state cause it is updated
        # asynchronously which causes the play buttons to flicker
        return self._playing

    def play(self, player):
        self._playing = True
        player.play(self._track.filename)

    def stop(self, player):
        self._playing = False
        player.stop()

    def remove(self):
        self._album.removeTrack(self._track)

    def insert(self, position):
        self._album.insertTrack(self._track, position)

    def moveTo(self, position):
        self.remove()
        self.insert(position)

    def trackStateChanged(self, track):
        self.signalRowChange()

    def started(self, filename):
        if filename == self._track.filename:
            self._playing = True
            self.signalRowChange()

    def paused(self, filename):
        self.stopped(filename)

    def stopped(self, filename):
        if filename == self._track.filename:
            self._playing = False
            self.signalRowChange()

    def signalRowChange(self):
        self.rowChanged.emit(self)

    def __eq__(self, other):
        return self._track == other._track


class Column(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class ColumnEnum(type):
    def __len__(cls):
        return len(cls.__values__)

    def index(cls, column):
        return cls.__values__.index(column)

    def __getitem__(cls, item):
        return cls.__values__[item]


class Columns:
    __metaclass__ = ColumnEnum

    # todo i18n on column names
    trackTitle = Column(name='Titre de la piste', value=lambda track: track.trackTitle)
    leadPerformer = Column(name='Artiste principal', value=Row.leadPerformer)
    releaseName = Column(name="Titre de l'album", value=Row.releaseName)
    bitrate = Column(name=u'Débit',
                     value=lambda track: '%s kbps' % display.inKbps(track.bitrate()))
    duration = Column(name=u'Durée',
                      value=lambda track: display.asDuration(track.duration()))
    play = Column(name='', value=Row.playing)
    remove = Column(name='', value=lambda track: None)

    __values__ = trackTitle, leadPerformer, releaseName, bitrate, duration, play, remove


class AlbumCompositionModel(QAbstractTableModel, AlbumListener, TrackListener):
    def __init__(self, album, player, parent=None):
        QAbstractTableModel.__init__(self, parent)

        self._album = album
        self._album.addAlbumListener(self)
        self._player = player
        self._tracks = []

    @property
    def tracks(self):
        return tuple(self._tracks)

    def columnCount(self, index=QModelIndex()):
        return len(Columns)

    def rowCount(self, parent=QModelIndex()):
        return len(self._tracks)

    def flags(self, index):
        return Qt.ItemFlags(Qt.ItemIsEnabled)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if not role == Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return Columns[section].name
        else:
            return str(section + 1)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._album)):
            return None

        if role != Qt.DisplayRole:
            return None

        return Columns[index.column()].value(self.trackAt(index.row()))

    def trackAt(self, position):
        return self._tracks[position]

    def togglePlay(self, track):
        if track.playing():
            track.stop(self._player)
        else:
            track.play(self._player)

    def remove(self, track):
        if track.playing():
            track.stop(self._player)
        track.remove()

    def move(self, fromPosition, toPosition):
        self.trackAt(fromPosition).moveTo(toPosition)

    def albumStateChanged(self, album):
        self.dataChanged.emit(self.index(0, Columns.index(Columns.leadPerformer)),
                              self.index(self.rowCount() - 1, Columns.index(Columns.releaseName)))

    def trackAdded(self, track, position):
        row = Row(self._album, track, self._inPlay(track))
        track.addTrackListener(row)
        self._player.addPlayerListener(row)
        self._tracks.insert(position, row)
        row.rowChanged.connect(self.rowChanged)
        self.insertRows(position, 1, QModelIndex())

    def rowChanged(self, row):
        position = self._tracks.index(row)
        self.dataChanged.emit(self.index(position, 0), self.index(position, len(Columns) - 1))

    def trackRemoved(self, track, position):
        row = self.trackAt(position)
        track.removeTrackListener(row)
        self._player.removePlayerListener(row)
        row.rowChanged.disconnect()
        self._tracks.remove(row)
        self.removeRows(position, 1, QModelIndex())

    def insertRows(self, position, rows, parent):
        self.beginInsertRows(parent, position, position + rows - 1)
        self.endInsertRows()

    def removeRows(self, position, rows, parent):
        self.beginRemoveRows(parent, position, position + rows - 1)
        self.endRemoveRows()

    def _inPlay(self, track):
        return self._player.isPlaying() and self._player.media == track.filename