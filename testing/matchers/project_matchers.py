# -*- coding: utf-8 -*-
from hamcrest import has_property, has_properties, anything


def snapshot_with_path(path):
    return has_property("path", path)


def snapshot_with(name=anything(), type_=anything(), path=anything(), cover_art=anything()):
    return has_properties(name=name, type=type_, path=path, cover_art=cover_art)


def project_with(name=anything(), path=anything(), main_artist=anything(), tracks=anything(), **properties):
    return has_properties(release_name=name, filename=path, lead_performer=main_artist, tracks=tracks, **properties)
