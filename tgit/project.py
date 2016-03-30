# -*- coding: utf-8 -*-
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
