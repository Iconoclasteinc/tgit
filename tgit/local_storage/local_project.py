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
from os.path import join, dirname

import tgit
from tgit.album import Album
from tgit.metadata import Metadata
from tgit.tagging import tagging
from tgit.util import fs
from . import naming, yaml


def load_album(filename):
    data = yaml.read_data(filename)

    metadata = Metadata(data)
    album = Album(metadata, of_type=data["type"], destination=filename)

    for image in data["images"]:
        album.addImage(image[0], fs.read(join(dirname(album.destination), image[1])), image[2], image[3])

    for track_filename in data["tracks"]:
        track_file = join(dirname(album.destination), track_filename)
        album.add_track(tagging.load_track(track_file))

    return album


def save_album(album, track_name=naming.track_scheme, track_catalog=tagging, artwork_name=naming.artwork_scheme):
    data = dict(album.metadata)
    data["version"] = tgit.__version__
    data["type"] = album.type
    data["images"] = [(image.mime, artwork_name(image), image.type, image.desc) for image in album.images]
    data["tracks"] = [track_name(track) for track in album.tracks]

    yaml.write_data(album.destination, data)

    for image in album.images:
        image_file = join(dirname(album.destination), artwork_name(image))
        fs.write(image_file, image.data)

    for track in album.tracks:
        track_file = join(dirname(album.destination), track_name(track))
        fs.copy(track.filename, track_file)
        track.filename = track_file
        track_catalog.save_track(track)
