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


class TextField():
    def __init__(self, field_name, tag_name):
        self._field_name = field_name
        self._tag_name = tag_name

    def read(self, fields, metadata):
        if self._field_name in fields:
            metadata[self._tag_name] = fields[self._field_name][-1]

    def write(self, metadata, fields):
        for field in fields:
            if field[0] == self._field_name:
                fields.remove(field)
        text = metadata[self._tag_name]
        if text:
            fields.append((self._field_name, text))


class FlacContainer():
    fields = []

    for field_name, tag_name in {
        'ARTIST': 'lead_performer',
        'TITLE': 'track_title',
    }.items():
        fields.append(TextField(field_name, tag_name))

    def load(self, filename):
        flac_file = mutagen.flac.FLAC(filename)

        metadata = Metadata()
        metadata['duration'] = flac_file.info.length
        metadata['bitrate'] = flac_file.info.sample_rate * flac_file.info.bits_per_sample

        for field in self.fields:
            field.read(flac_file, metadata)

        return metadata

    def save(self, filename, metadata):
        flac_file = self._load_file(filename)

        for field in self.fields:
            field.write(metadata, flac_file.tags)

        flac_file.save(filename)


    @staticmethod
    def _load_file(filename):
        try:
            return mutagen.flac.FLAC(filename)
        except mutagen.flac.FLACNoHeaderError:
            return mutagen.flac.FLAC()