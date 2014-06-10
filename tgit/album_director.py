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

from tgit.util import fs


class Snapshot(object):
    def __str__(self):
        return str(self.__dict__)


def updateTrack(track, state):
    track.trackTitle = state.trackTitle
    track.leadPerformer = state.leadPerformer
    track.versionInfo = state.versionInfo
    track.featuredGuest = state.featuredGuest
    track.lyricist = state.lyricist
    track.composer = state.composer
    track.publisher = state.publisher
    track.isrc = state.isrc
    track.tags = state.tags
    track.lyrics = state.lyrics
    track.language = state.language


def updateAlbum(album, state):
    album.releaseName = state.releaseName
    album.compilation = state.compilation
    album.leadPerformer = state.leadPerformer
    album.guestPerformers = state.guestPerformers
    album.labelName = state.labelName
    album.catalogNumber = state.catalogNumber
    album.upc = state.upc
    album.comments = state.comments
    album.releaseTime = state.releaseTime
    album.recordingTime = state.recordingTime
    album.recordingStudios = state.recordingStudios
    album.producer = state.producer
    album.mixer = state.mixer
    album.primaryStyle = state.primaryStyle


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