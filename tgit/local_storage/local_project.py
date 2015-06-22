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
    metadata.addImages(*data["images"])
    album = Album(metadata, of_type=data["type"], destination=filename)

    for track_filename in data["tracks"]:
        track_file = join(dirname(album.destination), track_filename)
        album.add_track(tagging.load_track(track_file))

    return album


def save_album(album, naming_scheme=naming.default_scheme, track_catalog=tagging):
    data = dict(album.metadata)
    data["version"] = tgit.__version__
    data["type"] = album.type
    data["images"] = album.metadata.images
    data["tracks"] = [naming_scheme(track) for track in album.tracks]

    yaml.write_data(album.destination, data)

    for track in album.tracks:
        track_file = join(dirname(album.destination), naming_scheme(track))
        fs.copy(track.filename, track_file)
        track.filename = track_file
        track_catalog.save_track(track)
