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
import shutil

from dateutil import tz

import requests
from yaml import dump, Dumper, load

import tgit
from tgit import tagging
from tgit.album import Album
from tgit.export.csv_format import CsvFormat
from tgit.metadata import Metadata
from tgit.track import Track
from tgit.util import fs


def create_album_into(portfolio):
    def build_full_path(creation_properties):
        return "{0}/{1}.tgit".format(creation_properties["album_location"], creation_properties["album_name"])

    def create_new_album(creation_properties):
        # todo: find a way to notify the portfolio's listeners of the destination
        album = Album(of_type=creation_properties["type"], destination=build_full_path(creation_properties))
        portfolio.add_album(album)
        return album

    def import_album_to_portfolio(creation_properties):
        _, extension = os.path.splitext(creation_properties["track_location"])
        all_metadata = tagging.load_metadata(creation_properties["track_location"])
        album_metadata = all_metadata.copy(*Album.tags())
        album = Album(album_metadata, of_type=creation_properties["type"],
                      destination=build_full_path(creation_properties))
        portfolio.add_album(album)
        add_tracks_to(album)(creation_properties["track_location"])
        return album

    def add_album(creation_properties):
        if creation_properties["track_location"]:
            album = import_album_to_portfolio(creation_properties)
        else:
            album = create_new_album(creation_properties)
        export_as_yaml(album)

    return add_album


def load_album_into(portfolio):
    def load_album(destination):
        album = import_from_yaml(destination)
        portfolio.add_album(album)

    return load_album


def remove_album_from(portfolio):
    def close_album(album):
        portfolio.remove_album(album)

    return close_album


def add_tracks_to(album):
    def add_tracks_to_album(*selection):
        for filename in selection:
            album.add_track(Track(filename, tagging.load_metadata(filename)))

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
        mime, data = fs.guess_mime_type(filename), fs.binary_content_of(filename)
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


def recordAlbum(album):
    for track in album.tracks:
        tag_track(tagged_file(album, track), track, datetime.now(tz.tzlocal()))


def tag_track(to_file, track, time):
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
        if to_file != track.filename:
            shutil.copy(track.filename, to_file)

    def save_track_metadata():
        tagging.save_metadata(to_file, track.metadata)

    update_track_metadata()
    copy_track_file()
    save_track_metadata()


def import_from_yaml(destination):
    with open(destination, "r") as album_file_stream:
        album_dict = load(album_file_stream)
        type_ = album_dict["type"]
        images = album_dict["images"]
        del album_dict["type"]
        del album_dict["images"]

        # todo: change the Metadata class to count images as tags.
        # We need to add the images to the metadata property after having created the album because the Album class
        # chooses to create a new Metadata instance
        album = Album(metadata=(Metadata(**album_dict)), of_type=type_, destination=destination)
        album.metadata.addImages(*images)
        return album


def export_as_yaml(album):
    with open(album.destination, "w") as out:
        metadata = dict(album.metadata)
        metadata["type"] = album.type
        metadata["images"] = album.metadata.images
        dump(metadata, stream=out, Dumper=Dumper, default_flow_style=False)


def export_as_csv(album):
    def export_album_as_csv(export_format, charset, destination):
        with open(destination, 'w', encoding=charset) as out:
            export_format.write(album, out)

    return functools.partial(export_album_as_csv, CsvFormat(), "windows-1252")


def tagged_file(album, track):
    dirname = os.path.dirname(album.destination)
    _, ext = os.path.splitext(track.filename)
    filename = fs.sanitize("{artist} - {number:02} - {title}{ext}".format(artist=track.lead_performer,
                                                                          number=track.track_number,
                                                                          title=track.track_title,
                                                                          ext=ext))

    return os.path.join(dirname, filename)


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
