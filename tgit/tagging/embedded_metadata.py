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

from tgit.metadata import Metadata
from tgit.tagging.flac_container import FlacContainer
from tgit.tagging.id3_container import ID3Container


containers = {
    '.mp3': ID3Container(),
    '.flac': FlacContainer()
}


class EmptyContainer(object):
    @staticmethod
    def load(filename):
        return Metadata()


    @staticmethod
    def save(filename, metadata):
        pass

_empty_container = EmptyContainer()


def _select_container(filename):
    for file_type, container in containers.items():
        if filename.endswith(file_type):
            return container

    return _empty_container


def load_metadata(filename):
    return _select_container(filename).load(filename)


def save_metadata(filename, metadata):
    return _select_container(filename).save(filename, metadata)
