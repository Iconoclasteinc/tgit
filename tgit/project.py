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
from tgit.album import Album
from tgit.metadata import Metadata
from tgit.tagging import tagging


def load_to(studio, portfolio, from_catalog=local_storage):
    def load_project(filename):
        project = from_catalog.load_project(filename)
        studio.project_loaded(project)
        portfolio.add_album(project)

    return load_project


def save_to(studio, catalog=local_storage):
    def save_project(project):
        catalog.save_project(project)
        studio.project_saved(project)

    return save_project


def create_in(studio, portfolio, to_catalog=local_storage, from_catalog=tagging):
    def create_project(type_, name, location, reference_track_file=None):
        reference_track = from_catalog.load_track(reference_track_file) if reference_track_file else None
        metadata = reference_track.metadata.copy() if reference_track else Metadata()
        metadata['release_name'] = name
        album = Album(of_type=type_, metadata=metadata, filename=os.path.join(location, name, "{0}.tgit".format(name)))
        if reference_track:
            album.add_track(reference_track)

        to_catalog.save_project(album)
        studio.project_created(album)
        portfolio.add_album(album)
        return album

    return create_project
