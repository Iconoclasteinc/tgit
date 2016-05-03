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


def album_exists(name, location, in_catalog=local_storage):
    return in_catalog.project_exists(os.path.join(location, name, "{0}.tgit".format(name)))


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

        track.update_chain_of_title()

    return update_track_metadata


def update_album_from(album):
    def update_album(**metadata):
        for key, value in metadata.items():
            setattr(album, key, value)

        if metadata.get("compilation") is True:
            album.lead_performer = ""
            album.lead_performer_region = None
            album.lead_performer_date_of_birth = "2000-01-01"
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
        return album.isnis[name] if album.isnis and name in album.isnis else ""

    return lookup_isni


def lookup_ipi_in(album):
    def lookup_ipi(name):
        return album.ipis[name] if album.ipis and name in album.ipis else ""

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
