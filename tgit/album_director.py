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
import functools
import os
import re
import shutil

from dateutil import tz
import requests

import tgit
from tgit import tagging
from tgit.album import Album
from tgit.export.csv_format import CsvFormat
from tgit.track import Track
from tgit.util import fs


def create_album(portfolio, of_type=Album.Type.FLAC):
    portfolio.add_album(Album(of_type=of_type))


def remove_album_from(portfolio):
    def close_album(album):
        portfolio.remove_album(album)

    return close_album


def import_album_to(portfolio):
    def import_album_to_portfolio(album_file):
        _, extension = os.path.splitext(album_file)
        all_metadata = tagging.load_metadata(album_file)
        album_metadata = all_metadata.copy(*Album.tags())
        album = Album(album_metadata, of_type=extension[1:])
        portfolio.add_album(album)
        add_tracks_to(album)([album_file])

    return import_album_to_portfolio


def add_tracks_to(album):
    def add_tracks_to_album(selection):
        for filename in list_audio_files_from(selection, of_type=".{}".format(album.type)):
            album.addTrack(Track(filename, tagging.load_metadata(filename)))

    return add_tracks_to_album


def updateTrack(track, **metadata):
    for key, value in metadata.items():
        setattr(track, key, value)


def updateAlbum(album, **metadata):
    for key, value in metadata.items():
        setattr(album, key, value)

    if not metadata.get('compilation'):
        for track in album.tracks:
            track.lead_performer = metadata.get('lead_performer')


def change_cover_of(album):
    def change_album_cover(filename):
        album.removeImages()
        mime, data = fs.guessMimeType(filename), fs.binary_content_of(filename)
        album.addFrontCover(mime, data)

    return change_album_cover


def removeAlbumCover(album):
    album.removeImages()


def moveTrack(album, track, position):
    album.removeTrack(track)
    album.insertTrack(track, position)


def remove_track_from(player, album):
    def remove_track_from_album(track):
        if player.is_playing(track):
            player.stop()

        album.removeTrack(track)

    return remove_track_from_album


def play_or_stop(player):
    def play_or_stop_track(track):
        if player.is_playing(track):
            player.stop()
        else:
            player.play(track)

    return play_or_stop_track


def recordAlbum(album):
    for track in album.tracks:
        record_track(tagged_name(track), track, datetime.now(tz.tzlocal()))


def record_track(destination_file, track, time):
    def album_metadata(album):
        metadata = album.metadata.copy()
        if album.compilation:
            del metadata['lead_performer']
        return metadata

    def update_track_metadata():
        track.tagger = 'TGiT'
        track.tagger_version = tgit.__version__
        track.tagging_time = time.strftime('%Y-%m-%d %H:%M:%S %z')
        track.metadata.update(album_metadata(track.album))

    def copy_track_file():
        if destination_file != track.filename:
            shutil.copy(track.filename, destination_file)

    def save_track_metadata():
        tagging.save_metadata(destination_file, track.metadata)

    update_track_metadata()
    copy_track_file()
    save_track_metadata()


def export_as_csv(album):
    def export_album_as_csv(export_format, charset, destination):
        with open(destination, 'w', encoding=charset) as out:
            export_format.write(album, out)

    return functools.partial(export_album_as_csv, CsvFormat(), "windows-1252")


def sanitize(filename):
    return re.sub(r'[/<>?*\\:|"]', '_', filename).strip()


def tagged_name(track):
    dirname = os.path.dirname(track.filename)
    _, ext = os.path.splitext(track.filename)
    filename = sanitize("{artist} - {number:02} - {title}{ext}".format(artist=track.lead_performer,
                                                                       number=track.track_number,
                                                                       title=track.track_title,
                                                                       ext=ext))

    return os.path.join(dirname, filename)


def list_audio_files_from(selection, of_type):
    files = []
    for filepath in selection:
        if os.path.isdir(filepath):
            files.extend(audio_files_in(filepath, of_type))
        else:
            files.append(filepath)
    return files


def audio_files_in(folder, of_type):
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(of_type)]


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
