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
from datetime import datetime, timezone

from tgit import __app_name__, __version__
from tgit.chain_of_title import ChainOfTitle
from tgit.track import Track
from . import embedded_containers as containers


def load_track(filename, chain_of_title=None):
    return Track(filename, containers.load_metadata(filename), chain_of_title)


def save_track(track, at_time=None):
    track.tagger = __app_name__
    track.tagger_version = __version__
    track.tagging_time = _in_utc(at_time).strftime("%Y-%m-%d %H:%M:%S %z")
    containers.save_metadata(track.filename, _all_metadata(track))


def _in_utc(at_time):
    return at_time and at_time.astimezone(timezone.utc) or datetime.now(timezone.utc)


def _all_metadata(track):
    album_metadata = track.album.metadata.copy()
    if track.album.compilation:
        del album_metadata["lead_performer"]
    track_metadata = track.metadata.copy()
    track_metadata.update(album_metadata)
    track_metadata["isnis"] = _clean_isnis(track_metadata)
    track_metadata["ipis"] = _clean_ipis(track_metadata)

    return track_metadata


def _clean_isnis(track_metadata):
    new_isni_map = {}
    isnis = track_metadata["isnis"] or {}

    lead_performer = track_metadata["lead_performer"]
    if lead_performer in isnis:
        new_isni_map[lead_performer] = isnis[lead_performer]

    _append_existing_identifiers(track_metadata["lyricist"] or [], isnis, new_isni_map)
    _append_existing_identifiers(track_metadata["composer"] or [], isnis, new_isni_map)
    _append_existing_identifiers(track_metadata["publisher"] or [], isnis, new_isni_map)

    return new_isni_map


def _clean_ipis(track_metadata):
    new_ipi_map = {}
    ipis = track_metadata["ipis"] or {}

    _append_existing_identifiers(track_metadata["lyricist"] or [], ipis, new_ipi_map)
    _append_existing_identifiers(track_metadata["composer"] or [], ipis, new_ipi_map)
    _append_existing_identifiers(track_metadata["publisher"] or [], ipis, new_ipi_map)

    return new_ipi_map


def _append_existing_identifiers(names, old_map, new_map):
    for name in names:
        if name in old_map:
            new_map[name] = old_map[name]
