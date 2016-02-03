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
from functools import wraps

from tgit import local_storage, fs
from tgit import tagging
from tgit.album import Album
from tgit.identity import IdentityCard


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

        if not metadata.get("compilation"):
            for track in album.tracks:
                track.lead_performer = metadata.get("lead_performer")

    return update_album


def change_cover_of(album):
    def change_album_cover(filename):
        album.remove_images()
        mime, data = fs.guess_mime_type(filename), fs.read(filename)
        album.add_front_cover(mime, data)

    return change_album_cover


def remove_album_cover_from(album):
    def remove_album_cover():
        album.remove_images()

    return remove_album_cover


def move_track_of(album):
    return album.move_track


def remove_track_from(album):
    return album.remove_track


def lookup_isni_using(cheddar, session):
    def lookup_isni(lead_performer, on_lookup_success):
        @_unwrap_future
        def on_lookup_done(identities):
            on_lookup_success([IdentityCard(**identity) for identity in identities])

        cheddar.get_identities(lead_performer, session.current_user.api_key).add_done_callback(on_lookup_done)

    return lookup_isni


def add_isni_to(album):
    def add_isni(name, isni):
        album.isnis = _add_identifier_to_map(album.isnis, isni, name)

    return add_isni


def lookup_isni_in(album):
    def lookup_isni(name):
        return album.isnis[name] if album.isnis and name in album.isnis else None

    return lookup_isni


def assign_isni_to_main_artist_using(cheddar, session, album):
    def assign_isni(type_, on_assign_success):
        titles = [track.track_title for track in album.tracks]
        _assign_isni(album.lead_performer, type_, titles, on_assign_success, cheddar, session.current_user)

    return assign_isni


def assign_isni_to_lyricist_using(cheddar, session):
    def assign_isni(track, on_assign_success):
        _assign_isni(track.lyricist, "individual", [track.track_title], on_assign_success, cheddar, session.current_user)

    return assign_isni


def _assign_isni(identity, type_, titles, on_success, cheddar, user):
    @_unwrap_future
    def on_assign_done(identity_details):
        on_success(IdentityCard(**identity_details))

    cheddar.assign_identifier(identity, type_, titles, user.api_key).add_done_callback(on_assign_done)


def add_ipi_to(album):
    def add_ipi(name, ipi):
        album.ipis = _add_identifier_to_map(album.ipis, ipi, name)

    return add_ipi


def _add_identifier_to_map(identifier_map, identifier, name):
    if not identifier_map:
        identifier_map = {}
    identifier_map[name] = identifier

    return identifier_map


def sign_in_using(authenticate, session):
    def sign_in(email, password):
        user = authenticate(email, password)
        session.login_as(user["email"], user["token"], user["permissions"])

    return sign_in


def sign_out_using(session):
    def sign_out():
        session.logout()

    return sign_out


def _unwrap_future(f):
    @wraps(f)
    def decorated(future):
        exception = future.exception()
        if exception:
            raise exception
        return f(future.result())

    return decorated


def update_preferences(preferences):
    def update_preferences_with(values):
        for key, value in values.items():
            setattr(preferences, key, value)

    return update_preferences_with
