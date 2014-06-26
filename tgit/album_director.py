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

from PyQt4.QtCore import QDir, QFileInfo
from tgit.album import Album

from tgit.util import fs


def createAlbum(portfolio):
    portfolio.addAlbum(Album())


def addTracksToAlbum(library, album, selection):
    for filename in mp3Files(selection):
        album.addTrack(library.fetch(filename))


def updateTrack(track, **metadata):
    for key, value in metadata.iteritems():
        setattr(track, key, value)


def updateAlbum(album, **metadata):
    for key, value in metadata.iteritems():
        setattr(album, key, value)

    if not metadata.get('compilation'):
        for track in album.tracks:
            track.leadPerformer = metadata.get('leadPerformer')


def changeAlbumCover(album, filename):
    album.removeImages()
    mime, data = fs.guessMimeType(filename), fs.readContent(filename)
    album.addFrontCover(mime, data)


def removeAlbumCover(album):
    album.removeImages()


def moveTrack(album, track, position):
    album.removeTrack(track)
    album.insertTrack(track, position)


def removeTrack(player, album, track):
    if player.isPlaying(track.filename):
        player.stop()

    album.removeTrack(track)


def playTrack(player, track):
    if player.isPlaying(track.filename):
        player.stop()
    else:
        player.play(track.filename)


def recordAlbum(catalog, album):
    for track in album.tracks:
        catalog.store(track)


def exportAlbum(format_, album, destination):
    with open(destination, 'wb') as out:
        format_.write(album, out)


#todo Consider moving to the library itself
def mp3Files(selection):
    files = []
    for filename in selection:
        if isDir(filename):
            files.extend(mp3FilesIn(QDir(filename)))
        else:
            files.append(filename)
    return files


def mp3FilesIn(folder):
    return [f.canonicalFilePath() for f in QDir(folder).entryInfoList(['*.mp3'])]


def isDir(filename):
    return QFileInfo(filename).isDir()
