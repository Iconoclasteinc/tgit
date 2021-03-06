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
import re
from collections import Counter

import mutagen.flac

from tgit.metadata import Metadata, Image
from ._pictures import PictureType

LAST = -1


def invert(mapping):
    return dict(list(zip(list(mapping.values()), list(mapping.keys()))))


class ValueField:
    def __init__(self, field_name, tag_name, field_to_tag, tag_to_field):
        self._field_name = field_name
        self._tag_name = tag_name
        self._to_tag = field_to_tag
        self._to_field = tag_to_field

    def read(self, flac, metadata):
        if self._field_name in flac:
            metadata[self._tag_name] = self._to_tag(flac[self._field_name])

    def write(self, metadata, flac):
        if self._field_name in flac:
            del flac[self._field_name]

        value = metadata[self._tag_name]
        if value is not None:
            flac[self._field_name] = self._to_field(value)


class SingleValueField(ValueField):
    def __init__(self, field_name, tag_name, field_to_tag, tag_to_field):
        super().__init__(field_name, tag_name, lambda values: field_to_tag(values[LAST]), tag_to_field)


class MultiValueTextField(ValueField):
    def __init__(self, field_name, tag_name):
        super().__init__(field_name, tag_name, lambda values: ", ".join(values), lambda tag: re.split(",\s*", tag))


class TextField(SingleValueField):
    def __init__(self, field_name, tag_name):
        super().__init__(field_name, tag_name, str, str)


class RegionField(SingleValueField):
    @staticmethod
    def to_region(value):
        return tuple(value.split(" "))

    @staticmethod
    def to_value(region):
        return " ".join(region)

    def __init__(self, field_name, tag_name):
        super().__init__(field_name, tag_name, self.to_region, self.to_value)


class NumericField(SingleValueField):
    def __init__(self, field_name, tag_name):
        super().__init__(field_name, tag_name, int, str)


class BooleanField(SingleValueField):
    @staticmethod
    def to_boolean(value):
        return value.lower() == "Yes".lower()

    @staticmethod
    def to_value(flag):
        return "Yes" if flag else "No"

    def __init__(self, field_name, tag_name):
        super().__init__(field_name, tag_name, self.to_boolean, self.to_value)


class PairField:
    def __init__(self, field_name, tag_name):
        self._field_name = field_name
        self._tag_name = tag_name

    def read(self, flac, metadata):
        if self._field_name not in flac:
            return

        metadata[self._tag_name] = []

        for entry in flac[self._field_name]:
            match = re.match(r"(?P<value>[^(]+)\s+\((?P<desc>[^)]+)\)", entry)

            if match:
                metadata[self._tag_name].append((match.group("desc"), match.group("value")))

    def write(self, metadata, flac):
        if self._field_name in flac:
            del flac[self._field_name]

        if self._tag_name not in metadata:
            return

        flac[self._field_name] = ["{} ({})".format(value, desc) for desc, value in metadata[self._tag_name]]


class SequenceField:
    def __init__(self, field_name, tag_name):
        self._field_name = field_name
        self._tag_name = tag_name

    def read(self, flac, metadata):
        if self._field_name not in flac:
            return

        metadata[self._tag_name] = flac[self._field_name]

    def write(self, metadata, flac):
        if self._field_name in flac:
            del flac[self._field_name]

        if self._tag_name not in metadata:
            return

        flac[self._field_name] = metadata[self._tag_name]


class PictureField:
    def __init__(self, field_name, image_types):
        self._picture_types = invert(image_types)
        self._image_types = image_types
        self._picture_types = invert(image_types)
        self._field_name = field_name

    def read(self, flac, metadata):
        for picture in flac.pictures:
            metadata.addImage(picture.mime, picture.data, self._image_types.get(picture.type, Image.OTHER),
                              picture.desc)

    def _pictures_in(self, metadata):
        image_count = Counter()

        for image in metadata.images:
            picture = mutagen.flac.Picture()
            picture.data = image.data
            picture.type = self._picture_types[image.type]
            picture.mime = image.mime
            image_count[image.desc] += 1
            if image_count[image.desc] > 1:
                picture.desc = image.desc + " ({0})".format(image_count[image.desc])
            else:
                picture.desc = image.desc

            yield picture

    def write(self, metadata, flac):
        flac.clear_pictures()
        for picture in self._pictures_in(metadata):
            flac.add_picture(picture)


class IdentifierField:
    def __init__(self, field_name, tag_name):
        self._tag_name = tag_name
        self._field_name = field_name

    def read(self, flac, metadata):
        if self._field_name not in flac:
            return

        metadata[self._tag_name] = {}
        identifiers = flac[self._field_name]
        for identifier_value in identifiers:
            identifier, name = self._deserialize_identifier(identifier_value)
            if identifier and name:
                metadata[self._tag_name][name] = identifier

    def write(self, metadata, flac):
        if self._tag_name not in metadata:
            return

        identifier_list = []
        for name, identifier in metadata[self._tag_name].items():
            identifier_list += ["{} ({})".format(identifier, name)]

        if len(identifier_list) > 0:
            flac[self._field_name] = identifier_list

    @staticmethod
    def _is_structured_representation(identifier):
        return identifier.rfind(":") >= 0

    def _deserialize_identifier(self, identifier):
        if self._is_structured_representation(identifier):
            return identifier.split(":")

        result = re.match("(.*) \((.*)\)", identifier)
        if result:
            return result.group(1), result.group(2)

        return "", ""


class FlacContainer:
    fields = [IdentifierField("ISNI", "isnis"),
              IdentifierField("IPI", "ipis"),
              PictureField("PICTURES", {
                  PictureType.OTHER: Image.OTHER,
                  PictureType.FRONT_COVER: Image.FRONT_COVER,
                  PictureType.BACK_COVER: Image.BACK_COVER,
              })]

    for field_name, tag_name in {
        "ALBUM": "release_name",
        "ARTIST": "lead_performer",
        "ORGANIZATION": "label_name",
        "GENRE": "primary_style",
        "DATE": "recording_time",
        "TITLE": "track_title",
        "ISRC": "isrc",
        "ISWC": "iswc",
        "TAGGER": "tagger",
        "TAGGER-VERSION": "tagger_version",
        "TAGGING-TIME": "tagging_time",
        "RECORDING-STUDIO": "recording_studio",
        "PRODUCER": "production_company",
        "MUSIC-PRODUCER": "music_producer",
        "CATALOGNUMBER": "catalog_number",
        "BARCODE": "upc",
        "MIXER": "mixer",
        "COMMENT": "comments",
        "VERSION": "version_info",
        "LYRICS": "lyrics",
        "LANGUAGE": "language",
        "GUEST ARTIST": "featured_guest",
        "TAG": "labels",
        "RELEASE DATE": "release_time",
        "LEAD-PERFORMER-DATE-OF-BIRTH": "lead_performer_date_of_birth",
        "RECORDING-STUDIO-ADDRESS": "recording_studio_address",
    }.items():
        fields.append(TextField(field_name, tag_name))

    for field_name, tag_name in {
        "LYRICIST": "lyricist",
        "PUBLISHER": "publisher",
        "COMPOSER": "composer",
    }.items():
        fields.append(SequenceField(field_name, tag_name))

    for field_name, tag_name in {
        "TAG": "labels",
    }.items():
        fields.append(MultiValueTextField(field_name, tag_name))

    for field_name, tag_name in {
        "TRACKNUMBER": "track_number",
        "TRACKTOTAL": "total_tracks",
    }.items():
        fields.append(NumericField(field_name, tag_name))

    for field_name, tag_name in {
        "LEAD-PERFORMER-REGION": "lead_performer_region",
        "RECORDING-STUDIO-REGION": "recording_studio_region",
        "PRODUCER-REGION": "production_company_region",
    }.items():
        fields.append(RegionField(field_name, tag_name))

    for field_name, tag_name in {
        "COMPILATION": "compilation",
    }.items():
        fields.append(BooleanField(field_name, tag_name))

    for field_name, tag_name in {
        "PERFORMER": "guest_performers",
    }.items():
        fields.append(PairField(field_name, tag_name))

    def load(self, filename):
        flac_file = mutagen.flac.FLAC(filename)

        metadata = Metadata()
        metadata["duration"] = flac_file.info.length
        metadata["bitrate"] = flac_file.info.sample_rate * flac_file.info.bits_per_sample

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
