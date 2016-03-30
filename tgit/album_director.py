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

from tgit import local_storage
from tgit import tagging
from tgit.album import Album


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
    return in_catalog.project_exists(_build_filename(name, location))


def save_album(to_catalog=local_storage):
    return to_catalog.save_project


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

    for current_filename in filenames:
        add_track(current_filename)


def add_tracks_to(album, from_catalog=tagging):
    return lambda *filenames: add_tracks(album, *filenames, from_catalog=from_catalog)


def update_track(track):
    def update_track_metadata(**metadata):
        for key, value in metadata.items():
            setattr(track, key, value)

    return update_track_metadata


def update_album_from(album):
    def update_album(**metadata):
        for key, value in metadata.items():
            setattr(album, key, value)

        if metadata.get("compilation") is True:
            album.lead_performer = ""
            for track in album.tracks:
                track.lead_performer = ""

        album_main_artist = metadata.get("lead_performer")
        if album_main_artist:
            for track in album.tracks:
                track.lead_performer = album_main_artist

    return update_album


def remove_album_cover_from(album):
    def remove_album_cover():
        album.remove_images()

    return remove_album_cover


def move_track_of(album):
    return album.move_track


def remove_track_from(album):
    return album.remove_track


def lookup_isni_in(album):
    def lookup_isni(name):
        return album.isnis[name] if album.isnis and name in album.isnis else None

    return lookup_isni


def lookup_ipi_in(album):
    def lookup_ipi(name):
        return album.ipis[name] if album.ipis and name in album.ipis else None

    return lookup_ipi


def add_ipi_to(album):
    def add_ipi(name, ipi):
        album.ipis = _add_identifier_to_map(album.ipis, ipi, name)

    return add_ipi


def _add_identifier_to_map(identifier_map, identifier, name):
    if not identifier_map:
        identifier_map = {}
    identifier_map[name] = identifier

    return identifier_map


def update_preferences(preferences):
    def update_preferences_with(values):
        for key, value in values.items():
            setattr(preferences, key, value)

    return update_preferences_with
