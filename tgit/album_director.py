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

from datetime import datetime
import os
import re
import shutil

from dateutil import tz
import requests

import tgit
from tgit import tagging
from tgit.album import Album
from tgit.track import Track
from tgit.util import fs


def createAlbum(portfolio):
    portfolio.addAlbum(Album())


def add_tracks_to_album(album, selection):
    for filename in list_audio_files_from(selection):
        album.addTrack(Track(filename, tagging.load_metadata(filename)))


def updateTrack(track, **metadata):
    for key, value in metadata.items():
        setattr(track, key, value)


def updateAlbum(album, **metadata):
    for key, value in metadata.items():
        setattr(album, key, value)

    if not metadata.get('compilation'):
        for track in album.tracks:
            track.lead_performer = metadata.get('lead_performer')


def changeAlbumCover(album, filename):
    album.removeImages()
    mime, data = fs.guessMimeType(filename), fs.binary_content_of(filename)
    album.addFrontCover(mime, data)


def removeAlbumCover(album):
    album.removeImages()


def moveTrack(album, track, position):
    album.removeTrack(track)
    album.insertTrack(track, position)


def removeTrack(player, album, track):
    if player.is_playing(track.filename):
        player.stop()

    album.removeTrack(track)


def playTrack(player, track):
    if player.is_playing(track.filename):
        player.stop()
    else:
        player.play(track.filename)


def recordAlbum(album):
    for track in album.tracks:
        record_track(taggedName(track), track, datetime.now(tz.tzlocal()))


def record_track(destination_file, track, time):
    track.tagger = 'TGiT v' + tgit.__version__
    track.taggingTime = time.strftime('%Y-%m-%d %H:%M:%S %z')
    metadata = track.metadata
    metadata.update(track.album.metadata)

    if destination_file != track.filename:
        shutil.copy(track.filename, destination_file)

    tagging.save_metadata(destination_file, metadata)


def export_album(export_format, album, destination, charset):
    with open(destination, 'w', encoding=charset) as out:
        export_format.write(album, out)


def sanitize(filename):
    return re.sub(r'[/<>?*\\:|"]', '_', filename).strip()


def taggedName(track):
    dirname = os.path.dirname(track.filename)
    _, ext = os.path.splitext(track.filename)
    filename = sanitize("{artist} - {number:02} - {title}{ext}".format(artist=track.lead_performer,
                                                                       number=track.number,
                                                                       title=track.track_title,
                                                                       ext=ext))

    return os.path.join(dirname, filename)


def list_audio_files_from(selection):
    files = []
    for filepath in selection:
        if os.path.isdir(filepath):
            files.extend(audio_files_in(filepath))
        else:
            files.append(filepath)
    return files


def audio_files_in(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.mp3') or f.endswith('flac')]


def lookupISNI(registry, leadPerformer):
    lastSpaceIndex = leadPerformer.rfind(' ')
    lastName = leadPerformer[lastSpaceIndex + 1:]
    restOfName = leadPerformer[:lastSpaceIndex]
    firstName = restOfName.split(' ')

    try:
        return registry.search_by_keywords(lastName, *firstName)
    except requests.exceptions.ConnectionError as e:
        return e


def selectISNI(identity, album):
    isni, personalInformations = identity
    leadPerformer, _, _ = personalInformations
    metadata = dict(lead_performer=leadPerformer, isni=isni, compilation=album.compilation)
    updateAlbum(album, **metadata)


def clearISNI(album):
    metadata = dict(isni=None)
    updateAlbum(album, **metadata)


def assign_isni(registry, album):
    lastSpaceIndex = album.lead_performer.rfind(' ')
    surname = album.lead_performer[lastSpaceIndex + 1:]
    forename = album.lead_performer[:lastSpaceIndex]

    return registry.assign(forename, surname, [album.release_name])
