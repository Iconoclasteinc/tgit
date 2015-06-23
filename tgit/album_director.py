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

import functools

import requests

from tgit import local_storage
from tgit import tagging
from tgit.album import Album
from tgit.local_storage.csv_format import CsvFormat
from tgit.util import fs


def _build_full_path(creation_properties):
    return "{0}/{1}.tgit".format(creation_properties["album_location"], creation_properties["album_name"])


def create_album_into(portfolio, to_catalog=local_storage):
    def create_new_album(creation_properties):
        album = Album(of_type=creation_properties["type"], destination=_build_full_path(creation_properties))
        save_album(to_catalog)(album)
        portfolio.add_album(album)
        return album

    return create_new_album


def import_album_into(portfolio, to_catalog=local_storage, from_catalog=tagging):
    def import_album_to_portfolio(creation_properties):
        reference_track = from_catalog.load_track(creation_properties["track_location"])
        album = Album(reference_track.metadata, of_type=creation_properties["type"],
                      destination=_build_full_path(creation_properties))
        add_tracks_to(album, from_catalog)(creation_properties["track_location"])
        save_album(to_catalog)(album)
        portfolio.add_album(album)
        return album

    return import_album_to_portfolio


def load_album_into(portfolio, from_catalog=local_storage):
    def load_album(filename):
        portfolio.add_album(from_catalog.load_album(filename))

    return load_album


def save_album(to_catalog=local_storage):
    return to_catalog.save_album


def remove_album_from(portfolio):
    def close_album(album):
        portfolio.remove_album(album)

    return close_album


def add_tracks_to(to_album, from_catalog=tagging):
    def add_tracks_from_catalog_to_album(*filename):
        for filename in filename:
            to_album.add_track(from_catalog.load_track(filename))

    return add_tracks_from_catalog_to_album


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
        mime, data = fs.guess_mime_type(filename), fs.read(filename)
        album.addFrontCover(mime, data)

    return change_album_cover


def removeAlbumCover(album):
    album.removeImages()


def move_track_of(album):
    def move_track_of_album(track, new_position):
        album.remove_track(track)
        album.insert_track(new_position, track)

    return move_track_of_album


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


def export_as_csv(album):
    def export_album_as_csv(export_format, charset, destination):
        with open(destination, 'w', encoding=charset) as out:
            export_format.write(album, out)

    return functools.partial(export_album_as_csv, CsvFormat(), "windows-1252")


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
