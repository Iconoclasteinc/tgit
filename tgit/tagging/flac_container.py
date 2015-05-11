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
from collections import Counter

import mutagen.flac

from tgit.metadata import Metadata, Image
from tgit.tagging._pictures import PictureType


LAST = -1


def invert(mapping):
    return dict(list(zip(list(mapping.values()), list(mapping.keys()))))


class TextField:
    def __init__(self, field_name, tag_name):
        self._field_name = field_name
        self._tag_name = tag_name

    def read(self, flac, metadata):
        if self._field_name in flac:
            metadata[self._tag_name] = flac[self._field_name][LAST]

    def write(self, metadata, flac):
        if self._field_name in flac:
            del flac[self._field_name]

        value = metadata[self._tag_name]
        if value:
            flac[self._field_name] = str(value)


class PictureField:
    def __init__(self, field_name, image_types):
        self._picture_types = invert(image_types)
        self._image_types = image_types
        self._picture_types = invert(image_types)
        self._field_name = field_name

    def read(self, flac, metadata):
        for picture in flac.pictures:
            metadata.addImage(picture.mime, picture.data, self._image_types.get(picture.type, Image.OTHER), picture.desc)

    def _pictures_in(self, metadata):
        image_count = Counter()

        for image in metadata.images:
            picture = mutagen.flac.Picture()
            picture.data = image.data
            picture.type = self._picture_types[image.type]
            picture.mime = image.mime
            image_count[image.desc] += 1
            if image_count[image.desc] > 1:
                picture.desc = image.desc + ' ({0})'.format(image_count[image.desc])
            else:
                picture.desc = image.desc

            yield picture

    def write(self, metadata, flac):
        flac.clear_pictures()
        for picture in self._pictures_in(metadata):
            flac.add_picture(picture)


class FlacContainer:
    fields = [PictureField('PICTURES', {
        PictureType.OTHER: Image.OTHER,
        PictureType.FRONT_COVER: Image.FRONT_COVER,
        PictureType.BACK_COVER: Image.BACK_COVER,
    })]

    for field_name, tag_name in {
        'ALBUM': 'release_name',
        'ARTIST': 'lead_performer',
        'ORGANIZATION': 'label_name',
        'GENRE': 'primary_style',
        'DATE': 'recording_time',
        'TITLE': 'track_title',
        'ISRC': 'isrc',
        'TAGGER': 'tagger',
        'TAGGER_VERSION': 'tagger_version',
        'TAGGING_TIME': 'tagging_time',
        'TRACKNUMBER': 'track_number',
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
            field.write(metadata, flac_file)

        flac_file.save(filename)


    @staticmethod
    def _load_file(filename):
        try:
            return mutagen.flac.FLAC(filename)
        except mutagen.flac.FLACNoHeaderError:
            return mutagen.flac.FLAC()