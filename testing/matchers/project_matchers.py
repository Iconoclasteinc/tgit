# -*- coding: utf-8 -*-
from hamcrest import has_property, has_properties, anything


def project_with_path(path):
    return has_property("filename", path)


def project_with(name=anything(), path=anything(), main_artist=anything(), tracks=anything(), **properties):
    return has_properties(release_name=name, filename=path, lead_performer=main_artist, tracks=tracks, **properties)
