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
from collections import defaultdict

from tgit.metadata import Metadata
from tgit.util import fs
from .flac_container import FlacContainer
from .id3_container import ID3Container


class EmptyContainer():
    @staticmethod
    def load(filename):
        return Metadata()

    @staticmethod
    def save(filename, metadata):
        pass


_containers = defaultdict(EmptyContainer, {".mp3": ID3Container(), ".flac": FlacContainer()})


def _container_for(filename):
    return _containers[fs.ext(filename)]


def load_metadata(filename):
    return _container_for(filename).load(filename)


def save_metadata(filename, metadata):
    return _container_for(filename).save(filename, metadata)
