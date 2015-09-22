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
import os

import requests

from tgit import local_storage
from tgit import tagging
from tgit.album import Album
from tgit.local_storage.csv_format import CsvFormat
from tgit.util import fs


def _build_filename(name, location):
    return os.path.join(location, name, "{0}.tgit".format(name))


def _must_import(filename):
    return len(filename) > 0


def _import(of_type, filename, reference_track_file, from_catalog):
    reference_track = from_catalog.load_track(reference_track_file)
    album = Album(of_type=of_type, filename=filename, metadata=reference_track.metadata)
    add_tracks(album, reference_track_file, from_catalog=from_catalog)
    return album


def _create_or_import_album(of_type, filename, reference_track_file, from_catalog):
    if _must_import(reference_track_file):
        return _import(of_type, filename, reference_track_file, from_catalog)
    return Album(of_type=of_type, filename=filename)


def create_album_into(portfolio, to_catalog=local_storage, from_catalog=tagging):
    def create_new_album(type_, name, location, reference_track_file=""):
        album = _create_or_import_album(type_, _build_filename(name, location), reference_track_file, from_catalog)
        album.release_name = name
        save_album(to_catalog)(album)
        portfolio.add_album(album)
        return album

    return create_new_album


def album_exists(name, location, in_catalog=local_storage):
    return in_catalog.album_exists(_build_filename(name, location))


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


def add_tracks(album, *filenames, from_catalog=tagging):
    def add_track(filename):
        try:
            album.add_track(from_catalog.load_track(filename))
        except Exception:
            pass

    for filename in filenames:
        add_track(filename)


def add_tracks_to(album, from_catalog=tagging):
    return lambda *filenames: add_tracks(album, *filenames, from_catalog=from_catalog)


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
    return album.move_track


def remove_track_from(album):
    return album.remove_track


def export_as_csv(album, destination):
    with open(destination, "w", encoding="windows-1252") as out:
        CsvFormat().write(album, out)


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


def sign_in(account):
    pass
