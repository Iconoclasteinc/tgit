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
import mutagen.flac

from tgit.metadata import Metadata


class FlacContainer(object):
    @staticmethod
    def load(filename):
        flac_file = mutagen.flac.FLAC(filename)

        metadata = Metadata()

        if 'ARTIST' in flac_file:
            metadata['leadPerformer'] = flac_file['ARTIST'][-1]

        return metadata

    @staticmethod
    def save(filename, metadata):
        flac_file = FlacContainer._load_file(filename)

        flac_file.tags.append(('ARTIST', metadata['leadPerformer']))

        flac_file.save(filename)


    @staticmethod
    def _load_file(filename):
        try:
            return mutagen.flac.FLAC(filename)
        except mutagen.flac.FLACNoHeaderError:
            return mutagen.flac.FLAC()