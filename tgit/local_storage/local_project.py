# -*- coding: utf-8 -*-
#
# TGiT, Music Tagger for Professionals
# Copyright (C) 2013 Iconoclaste Musique Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.qp6
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
from os.path import join, dirname

import tgit
from tgit.album import Album
from tgit.metadata import Metadata
from tgit.tagging import tagging
from tgit.util import fs
from . import naming, yaml

ARTWORK_FOLDER_NAME = "Artwork"
TRACKS_FOLDER_NAME = "Tracks"


def album_exists(filename):
    return os.path.exists(filename)


def load_album(filename):
    album_folder = dirname(filename)
    tracks_folder = join(album_folder, TRACKS_FOLDER_NAME)
    artwork_folder = join(album_folder, ARTWORK_FOLDER_NAME)

    data = yaml.read_data(filename)
    album = Album(Metadata(data), of_type=data["type"], filename=filename)

    for image in data["images"]:
        mime, filename, type_, desc = image
        album.add_image(mime, fs.read(join(artwork_folder, filename)), type_, desc)

    for track_filename in data["tracks"]:
        track_file = join(tracks_folder, track_filename)
        album.add_track(tagging.load_track(track_file))

    return album


def save_album(album, track_name=naming.track_scheme, track_catalog=tagging, artwork_name=naming.artwork_scheme):
    album_folder = dirname(album.filename)
    tracks_folder = join(album_folder, TRACKS_FOLDER_NAME)
    artwork_folder = join(album_folder, ARTWORK_FOLDER_NAME)

    def save_album_data():
        data = dict(album.metadata)
        data["version"] = tgit.__version__
        data["type"] = album.type
        data["images"] = [(image.mime, artwork_name(image), image.type, image.desc) for image in album.images]
        data["tracks"] = [track_name(track) for track in album.tracks]

        fs.mkdirs(album_folder)
        yaml.write_data(album.filename, data)

    def save_album_artwork():
        fs.mkdirs(artwork_folder)
        fs.remove_files(artwork_folder)

        for image in album.images:
            artwork_file = join(artwork_folder, artwork_name(image))
            fs.write(artwork_file, image.data)

    def save_tracks():
        fs.mkdirs(tracks_folder)

        for track in album.tracks:
            track_file = join(tracks_folder, track_name(track))
            fs.copy(track.filename, track_file)
            track.filename = track_file
            track_catalog.save_track(track)

        fs.remove_files(tracks_folder, lambda filename: filename not in (track.filename for track in album.tracks))

    save_album_data()
    save_album_artwork()
    save_tracks()
