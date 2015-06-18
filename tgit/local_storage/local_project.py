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

from yaml import dump, Dumper, load

from tgit.album import Album
from tgit.metadata import Metadata


def load_album(filename):
    metadata = _load_album_data_from_yaml(filename)
    # todo: change the Metadata class to count images as tags.
    # We need to add the images to the metadata property after having created the album because the Album class
    # chooses to create a new Metadata instance
    album = Album(metadata, of_type=metadata["type"], destination=filename)
    return album


def save_album(album):
    data = dict(album.metadata)
    data["type"] = album.type
    data["images"] = album.metadata.images
    _save_album_data_to_yaml(album.destination, data)


def _load_album_data_from_yaml(filename):
    with open(filename, "r") as album_file:
        data = load(album_file)

    metadata = Metadata(data)
    metadata.addImages(*data["images"])
    return metadata


def _save_album_data_to_yaml(filename, data):
    with open(filename, "w") as album_file:
        dump(data, stream=album_file, Dumper=Dumper, default_flow_style=False)



