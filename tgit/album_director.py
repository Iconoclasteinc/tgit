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
from queue import Queue
import threading

from PyQt5.QtCore import QEventLoop

from PyQt5.QtWidgets import QApplication
import requests

from identity import Identity
from isni.name_registry import NameRegistry
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
        album.removeImages()
        mime, data = fs.guess_mime_type(filename), fs.read(filename)
        album.add_front_cover(mime, data)

    return change_album_cover


def remove_album_cover_from(album):
    def remove_album_cover():
        album.removeImages()
    return remove_album_cover


def move_track_of(album):
    return album.move_track


def remove_track_from(album):
    return album.remove_track


def export_as_csv(album, destination):
    with open(destination, "w", encoding="windows-1252") as out:
        CsvFormat().write(album, out)


def lookup_isni_using(cheddar, user):
    def lookup_isni(lead_performer, on_successful_lookup):
        def poll_queue():
            while queue.empty():
                QApplication.processEvents(QEventLoop.AllEvents, 100)
            return queue.get(True)

        queue = Queue()

        try:
            threading.Thread(target=lambda: queue.put(cheddar.get_identities(lead_performer, user.api_key))).start()
            on_successful_lookup([Identity(**identity) for identity in poll_queue()])
        except requests.exceptions.ConnectionError as e:
            return on_successful_lookup(e)
    return lookup_isni


def select_isni_in(album):
    def select_isni(identity):
        metadata = dict(lead_performer=identity.full_name, isni=identity.id, compilation=album.compilation)
        update_album_from(album)(**metadata)
    return select_isni


def clear_isni_from(album):
    def clear_isni():
        metadata = dict(isni=None)
        update_album_from(album)(**metadata)
    return clear_isni


def assign_isni_using(registry):
    def assign_isni(lead_performer, release_name, on_successful_lookup):
        last_space_index = lead_performer.rfind(" ")
        surname = lead_performer[last_space_index + 1:]
        forename = lead_performer[:last_space_index]

        def poll_queue():
            while queue.empty():
                QApplication.processEvents(QEventLoop.AllEvents, 100)
            return queue.get(True)

        queue = Queue()

        try:
            threading.Thread(target=lambda: queue.put(registry.assign(forename, surname, [release_name]))).start()
            on_successful_lookup(poll_queue())
        except requests.exceptions.ConnectionError as e:
            return on_successful_lookup((NameRegistry.Codes.ERROR, str(e)))
    return assign_isni


def sign_in_using(authenticate, session):
    def sign_in(email, password):
        user = authenticate(email, password)
        session.login_as(user["email"], user["token"])

    return sign_in


def sign_out_using(session):
    def sign_out():
        session.logout()

    return sign_out
