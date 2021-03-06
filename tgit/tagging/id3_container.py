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
from datetime import timezone

from dateutil import parser as dateparser
from mutagen import mp3, id3

from tgit.metadata import Metadata, Image
from ._pictures import PictureType


def invert(mapping):
    return dict(list(zip(list(mapping.values()), list(mapping.keys()))))


def _decompose(key):
    parts = (key + "::").split(":")
    return parts[0], parts[1], parts[2]


class TextProcessor:
    def __init__(self, key, tag, frame_to_tag, tag_to_frame, optional_description=None):
        self._optional_description = optional_description
        self._key = key
        self._tag = tag
        self._to_tag = frame_to_tag
        self._to_frame = tag_to_frame

    def process_frames(self, metadata, frames):
        key = self._key
        if self._optional_description is not None:
            key += ":{}".format(self._optional_description)

        if key in frames:
            frame = frames[key]
            metadata[self._tag] = self._to_tag(frame)

    def process_metadata(self, frames, encoding, metadata):
        frame, desc, lang = _decompose(self._key)
        text = metadata[self._tag]
        frames.delall(self._key)
        if text:
            description = desc
            if self._optional_description is not None:
                description += ":{}".format(self._optional_description)
            frames.add(getattr(id3, frame)(encoding=encoding, desc=description, lang=lang, text=self._to_frame(text)))


class UnicodeProcessor(TextProcessor):
    def __init__(self, key, tag):
        super().__init__(key, tag, str, str)


class BooleanProcessor(TextProcessor):
    @staticmethod
    def to_boolean(frame):
        return str(frame) == "1"

    @staticmethod
    def to_text(value):
        return value and "1" or "0"

    def __init__(self, key, tag):
        super().__init__(key, tag, self.to_boolean, self.to_text)


class RegionProcessor(TextProcessor):
    @staticmethod
    def to_region(frame):
        return tuple(str(frame).split(" "))

    @staticmethod
    def to_text(value):
        return " ".join(value)

    def __init__(self, key, tag):
        super().__init__(key, tag, self.to_region, self.to_text, optional_description="UN/LOCODE")


class SequenceProcessor(TextProcessor):
    @staticmethod
    def to_sequence(frame):
        return [str(text) for text in frame.text]

    @staticmethod
    def to_text(value):
        return [str(current_value) for current_value in value]

    def __init__(self, key, tag):
        super().__init__(key, tag, self.to_sequence, self.to_text)


class MultiValueNumericProcessor:
    def __init__(self, key, *tags):
        self._key = key
        self._tags = tags

    def process_frames(self, metadata, frames):
        if self._key in frames:
            values = frames[self._key][0].split("/")

            for index, value in enumerate(values):
                if index < len(self._tags):
                    metadata[self._tags[index]] = int(value)

    def process_metadata(self, frames, encoding, metadata):
        frame, desc, lang = _decompose(self._key)
        frames.delall(self._key)
        value = "/".join(str(metadata[tag]) for tag in self._tags if metadata[tag])
        if value:
            frames.add(getattr(id3, frame)(encoding=encoding, desc=desc, lang=lang, text=value))


class ImageProcessor:
    def __init__(self, key, image_types):
        self._key = key
        self._picture_types = invert(image_types)
        self._image_types = image_types

    def process_frames(self, metadata, frames):
        for key in self._picture_frames(frames):
            picture = frames[key]
            image_type = self._image_types.get(picture.type, Image.OTHER)
            metadata.addImage(picture.mime, picture.data, image_type, picture.desc)

    def _picture_frames(self, frames):
        return [key for key in frames if key.startswith(self._key)]

    def _pictures_in(self, metadata, encoding):
        image_count = Counter()
        for image in metadata.images:
            image_count[image.desc] += 1
            if image_count[image.desc] > 1:
                description = image.desc + " ({0})".format(image_count[image.desc])
            else:
                description = image.desc

            yield getattr(id3, self._key)(encoding=encoding, mime=image.mime,
                                          type=self._picture_types[image.type],
                                          desc=description, data=image.data)

    def process_metadata(self, frames, encoding, metadata):
        frames.delall(self._key)

        for picture in self._pictures_in(metadata, encoding):
            frames.add(picture)


class PairProcessor:
    def __init__(self, key, tag, roles):
        self._key = key
        self._tag = tag
        self._roles = roles

    def process_frames(self, metadata, frames):
        if self._key in frames:
            metadata[self._tag] = []
            frame = frames[self._key]
            for role, name in self._known_id3_roles(self._significant_roles(frame.people)):
                metadata[role] = name
            for role, name in self._other_id3_roles(self._significant_roles(frame.people)):
                metadata[self._tag].append((role, name))

    @staticmethod
    def _significant_roles(pairs):
        return [(role, name) for role, name in pairs if name]

    def _known_id3_roles(self, pairs):
        return [(self._roles[role], name) for role, name in pairs if role in self._roles]

    def _other_id3_roles(self, pairs):
        return [(role, name) for role, name in pairs if role not in self._roles]

    def process_metadata(self, frames, encoding, metadata):
        frame = getattr(id3, self._key)(encoding=encoding)
        frame.people.extend(self._significant_roles(self._known_metadata_roles(metadata)))
        frame.people.extend(self._significant_roles(self._other_metadata_roles(metadata)))
        frames.add(frame)

    def _known_metadata_roles(self, metadata):
        return [[role, metadata[tag]] for role, tag in self._roles.items()
                if tag in metadata]

    def _other_metadata_roles(self, metadata):
        if self._tag not in metadata:
            return []
        return [[role, name] for role, name in metadata[self._tag]]


class IdentifierProcessor:
    def __init__(self, field_name, tag_name, prefix):
        self._prefix = prefix
        self._tag_name = tag_name
        self._field_name = field_name

    def process_frames(self, metadata, frames):
        identifier_map = {}
        for _, frame in frames.items():
            identifier_map = self._add_identifier_to_map(frame, identifier_map)

        if self._is_not_empty(identifier_map):
            metadata[self._tag_name] = identifier_map

    def process_metadata(self, frames, encoding, metadata):
        if self._tag_name not in metadata:
            return

        for _, frame in frames.items():
            if frame.FrameID == self._field_name and frame.desc.startswith(self._prefix):
                frames.delall("{}:{}".format(frame.FrameID, frame.desc))

        for name, identifier in metadata[self._tag_name].items():
            frames.add(getattr(id3, self._field_name)(encoding=encoding,
                                                      desc="{}:{}".format(self._prefix, name),
                                                      text=identifier))

    @staticmethod
    def _is_not_empty(identifiers):
        return len(identifiers) > 0

    def _add_identifier_to_map(self, frame, identifier_map):
        def is_identifier_frame():
            return frame.FrameID == self._field_name and frame.desc.startswith(self._prefix)

        def frame_is_not_empty():
            return len(frame.text) > 0

        if is_identifier_frame() and frame_is_not_empty():
            identifier_map[frame.desc.split(":")[1]] = frame.text[0]

        return identifier_map


class TaggerAndVersionConverter:
    def __init__(self, old_frame_key, tagger_frame, version_frame):
        self._old_frame_key = old_frame_key
        self._tagger_frame = tagger_frame
        self._version_frame = version_frame

    # noinspection PyUnusedLocal
    def process_frames(self, metadata, frames):
        if self._old_frame_key in frames:
            old = frames.pop(self._old_frame_key)
            import re
            match = re.match(r"(?P<tagger>[a-zA-Z_][a-zA-Z_0-9]+)\s+v(?P<version>[0-9\.]+)", str(old))

            frame, desc, lang = _decompose(self._tagger_frame)
            frames.add(getattr(id3, frame)(encoding=old.encoding, desc=desc, lang=lang, text=match.group("tagger")))

            frame, desc, lang = _decompose(self._version_frame)
            frames.add(getattr(id3, frame)(encoding=old.encoding, desc=desc, lang=lang, text=match.group("version")))

    # noinspection PyUnusedLocal
    def process_metadata(self, frames, encoding, metadata):
        frames.delall(self._old_frame_key)


class TextConverter:
    def __init__(self, old_key, new_key):
        self._old_key = old_key
        self._new_key = new_key

    # noinspection PyUnusedLocal
    def process_frames(self, metadata, frames):
        if self._old_key in frames:
            old = frames.pop(self._old_key)
            frame, desc, lang = _decompose(self._new_key)
            frames.add(getattr(id3, frame)(encoding=old.encoding, desc=desc, lang=lang, text=old.text))

    # noinspection PyUnusedLocal
    def process_metadata(self, frames, encoding, metadata):
        frames.delall(self._old_key)


class LocalDateTimeConverter:
    def __init__(self, old_key, new_key):
        self._old_key = old_key
        self._new_key = new_key

    # noinspection PyUnusedLocal
    def process_frames(self, metadata, frames):
        if self._old_key in frames:
            old = frames.pop(self._old_key)
            frame, desc, lang = _decompose(self._new_key)
            frames.add(getattr(id3, frame)(encoding=old.encoding, desc=desc, lang=lang,
                                           text=[self._to_timestamp(instant) for instant in old.text]))

    @staticmethod
    def _to_timestamp(value):
        instant = dateparser.parse(value).astimezone(timezone.utc)
        return instant.strftime("%Y-%m-%d %H:%M:%S")

    # noinspection PyUnusedLocal
    def process_metadata(self, frames, encoding, metadata):
        frames.delall(self._old_key)


class ISNIConverter:
    # noinspection PyUnusedLocal
    @staticmethod
    def process_frames(metadata, frames):
        if "TXXX:ISNI" not in frames:
            return

        isni = frames.pop("TXXX:ISNI")
        lead_performer = frames["TPE1"]
        frames.add(getattr(id3, "TXXX")(encoding=isni.encoding,
                                        desc="ISNI:{}".format(lead_performer.text[0]),
                                        text=isni.text[0]))

    # noinspection PyUnusedLocal
    @staticmethod
    def process_metadata(frames, encoding, metadata):
        frames.delall("TXXX:ISNI")


class ID3Container:
    UTF_8 = 3

    _upgraders = [
        TaggerAndVersionConverter("TXXX:Tagger", "TXXX:TAGGER", "TXXX:TAGGER_VERSION"),
        TextConverter("TXXX:UPC", "TXXX:BARCODE"),
        LocalDateTimeConverter("TXXX:Tagging Time", "TDTG"),
        LocalDateTimeConverter("TXXX:TAGGING_TIME", "TDTG"),
        ISNIConverter()
    ]

    _processors = [
        ImageProcessor("APIC", {
            PictureType.OTHER: Image.OTHER,
            PictureType.FRONT_COVER: Image.FRONT_COVER,
            PictureType.BACK_COVER: Image.BACK_COVER,
        }),
        IdentifierProcessor("TXXX", "isnis", "ISNI"),
        IdentifierProcessor("TXXX", "ipis", "IPI"),
        PairProcessor("TMCL", "guest_performers", {}),
        PairProcessor("TIPL", "contributors", {
            "producer": "music_producer",
            "mix": "mixer"
        }),
        MultiValueNumericProcessor("TRCK", "track_number", "total_tracks")
    ]

    for key, tag in {
        "TCMP": "compilation"
    }.items():
        _processors.append(BooleanProcessor(key, tag))

    for key, tag in {
        "TALB": "release_name",
        "TPE1": "lead_performer",
        "TOWN": "label_name",
        "TDRC": "recording_time",
        "TDRL": "release_time",
        "TDOR": "original_release_time",
        "TDTG": "tagging_time",
        "TIT2": "track_title",
        "TPE4": "version_info",
        "TSRC": "isrc",
        "TLAN": "language",
        "TXXX:BARCODE": "upc",
        "TXXX:Catalog Number": "catalog_number",
        "TXXX:Featured Guest": "featured_guest",
        "TXXX:PRODUCTION-COMPANY": "production_company",
        "TXXX:ISWC": "iswc",
        "TXXX:Recording Studio": "recording_studio",
        "TXXX:TAGGER": "tagger",
        "TXXX:TAGGER_VERSION": "tagger_version",
        "TXXX:Tags": "labels",
        "TXXX:LEAD-PERFORMER-DATE-OF-BIRTH": "lead_performer_date_of_birth",
        "TXXX:RECORDING-STUDIO-ADDRESS": "recording_studio_address",
        "COMM::fra": "comments",
        "USLT::fra": "lyrics",
        "TCON": "primary_style"
    }.items():
        _processors.append(UnicodeProcessor(key, tag))

    for key, tag in {
        "TEXT": "lyricist",
        "TCOM": "composer",
        "TPUB": "publisher",
    }.items():
        _processors.append(SequenceProcessor(key, tag))

    for key, tag in {
        "TXXX:LEAD-PERFORMER-REGION": "lead_performer_region",
        "TXXX:PRODUCTION-COMPANY-REGION": "production_company_region",
        "TXXX:RECORDING-STUDIO-REGION": "recording_studio_region",
    }.items():
        _processors.append(RegionProcessor(key, tag))

    _all_processors = _upgraders + _processors

    def __init__(self, encoding=UTF_8, overwrite=False):
        self._encoding = encoding
        self._overwrite = overwrite

    def load(self, filename):
        audio_file = mp3.MP3(filename)

        frames = audio_file.tags or {}

        metadata = Metadata()
        metadata["duration"] = audio_file.info.length
        metadata["bitrate"] = audio_file.info.bitrate

        for processor in self._all_processors:
            processor.process_frames(metadata, frames)

        return metadata

    def save(self, filename, metadata):
        frames = self._load_frames(filename)
        if self._overwrite:
            frames.clear()

        for processor in self._all_processors:
            processor.process_metadata(frames, self._encoding, metadata)

        frames.save(filename)

    @staticmethod
    def _load_frames(filename):
        try:
            return id3.ID3(filename)
        except id3.ID3NoHeaderError:
            return id3.ID3()
