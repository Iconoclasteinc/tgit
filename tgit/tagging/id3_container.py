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

from mutagen import mp3, id3

from tgit.metadata import Metadata, Image
from tgit.tagging._pictures import PictureType


def invert(mapping):
    return dict(list(zip(list(mapping.values()), list(mapping.keys()))))


def _decompose(key):
    parts = (key + '::').split(':')
    return parts[0], parts[1], parts[2]


class TextProcessor(object):
    def __init__(self, key, tag, frameToTag, tagToFrame):
        self._key = key
        self._tag = tag
        self._toTag = frameToTag
        self._toFrame = tagToFrame

    def processFrames(self, metadata, frames):
        if self._key in frames:
            frame = frames[self._key]
            metadata[self._tag] = self._toTag(frame)

    def processMetadata(self, frames, encoding, metadata):
        frame, desc, lang = _decompose(self._key)
        text = metadata[self._tag]
        frames.delall(self._key)
        if text:
            frames.add(getattr(id3, frame)(encoding=encoding, desc=desc, lang=lang, text=self._toFrame(text)))


class UnicodeProcessor(TextProcessor):
    def __init__(self, key, tag):
        super(UnicodeProcessor, self).__init__(key, tag, str, str)


class BooleanProcessor(TextProcessor):
    @staticmethod
    def toBoolean(text):
        return text == '1'

    @staticmethod
    def toText(value):
        return value and '1' or '0'

    def __init__(self, key, tag):
        super(BooleanProcessor, self).__init__(key, tag, self.toBoolean, self.toText)


class MultiValueNumericProcessor(object):
    def __init__(self, key, *tags):
        self._key = key
        self._tags = tags

    def processFrames(self, metadata, frames):
        if self._key in frames:
            values = frames[self._key][0].split("/")

            for index, value in enumerate(values):
                if index < len(self._tags):
                    metadata[self._tags[index]] = int(value)

    def processMetadata(self, frames, encoding, metadata):
        frame, desc, lang = _decompose(self._key)
        frames.delall(self._key)
        value = "/".join(str(metadata[tag]) for tag in self._tags if metadata[tag])
        if value:
            frames.add(getattr(id3, frame)(encoding=encoding, desc=desc, lang=lang, text=value))


class ImageProcessor(object):
    def __init__(self, key, image_types):
        self._key = key
        self._picture_types = invert(image_types)
        self._image_types = image_types

    def processFrames(self, metadata, frames):
        for key in self._pictureFrames(frames):
            picture = frames[key]
            imageType = self._image_types.get(picture.type, Image.OTHER)
            metadata.addImage(picture.mime, picture.data, imageType, picture.desc)

    def _pictureFrames(self, frames):
        return [key for key in frames if key.startswith(self._key)]

    def _pictures_in(self, metadata, encoding):
        image_count = Counter()
        for image in metadata.images:
            image_count[image.desc] += 1
            if image_count[image.desc] > 1:
                description = image.desc + ' ({0})'.format(image_count[image.desc])
            else:
                description = image.desc

            yield getattr(id3, self._key)(encoding=encoding, mime=image.mime,
                                          type=self._picture_types[image.type],
                                          desc=description, data=image.data)

    def processMetadata(self, frames, encoding, metadata):
        frames.delall(self._key)

        for picture in self._pictures_in(metadata, encoding):
            frames.add(picture)


class PairProcessor(object):
    def __init__(self, key, tag, roles):
        self._key = key
        self._tag = tag
        self._roles = roles

    def processFrames(self, metadata, frames):
        if self._key in frames:
            metadata[self._tag] = []
            frame = frames[self._key]
            for role, name in self._knownId3Roles(self._significantRoles(frame.people)):
                metadata[role] = name
            for role, name in self._otherId3Roles(self._significantRoles(frame.people)):
                metadata[self._tag].append((role, name))

    def _significantRoles(self, pairs):
        return [(role, name) for role, name in pairs if name]

    def _knownId3Roles(self, pairs):
        return [(self._roles[role], name) for role, name in pairs if role in self._roles]

    def _otherId3Roles(self, pairs):
        return [(role, name) for role, name in pairs if role not in self._roles]

    def processMetadata(self, frames, encoding, metadata):
        frame = getattr(id3, self._key)(encoding=encoding)
        frame.people.extend(self._significantRoles(self._knownMetadataRoles(metadata)))
        frame.people.extend(self._significantRoles(self._otherMetadataRoles(metadata)))
        frames.add(frame)

    def _knownMetadataRoles(self, metadata):
        return [[role, metadata[tag]] for role, tag in self._roles.items()
                if tag in metadata]

    def _otherMetadataRoles(self, metadata):
        if self._tag not in metadata:
            return []
        return [[role, name] for role, name in metadata[self._tag]]


class TaggerAndVersionProcessor:
    def __init__(self, old_frame_key, tagger_frame, version_frame):
        self._old_frame_key = old_frame_key
        self._tagger_frame = tagger_frame
        self._version_frame = version_frame

    def processFrames(self, metadata, frames):
        if self._old_frame_key in frames:
            old = frames.pop(self._old_frame_key)
            import re
            match = re.match(r'(?P<tagger>[a-zA-Z_][a-zA-Z_0-9]+)\s+v(?P<version>[0-9\.]+)', str(old))

            frame, desc, lang = _decompose(self._tagger_frame)
            frames.add(getattr(id3, frame)(encoding=old.encoding, desc=desc, lang=lang, text=match.group('tagger')))

            frame, desc, lang = _decompose(self._version_frame)
            frames.add(getattr(id3, frame)(encoding=old.encoding, desc=desc, lang=lang, text=match.group('version')))

    def processMetadata(self, frames, encoding, metadata):
        frames.delall(self._old_frame_key)


class UpgradeProcessor:
    def __init__(self, old_key, new_key):
        self._old_key = old_key
        self._new_key = new_key

    def processFrames(self, metadata, frames):
        if self._old_key in frames:
            old = frames.pop(self._old_key)
            frame, desc, lang = _decompose(self._new_key)
            frames.add(getattr(id3, frame)(encoding=old.encoding, desc=desc, lang=lang, text=old.text))

    def processMetadata(self, frames, encoding, metadata):
        frames.delall(self._old_key)


class ID3Container:
    UTF_8 = 3

    _upgraders = [
        TaggerAndVersionProcessor('TXXX:Tagger', 'TXXX:TAGGER', 'TXXX:TAGGER_VERSION'),
        UpgradeProcessor('TXXX:UPC', 'TXXX:BARCODE'),
        UpgradeProcessor('TXXX:Tagging Time', 'TXXX:TAGGING_TIME')
    ]

    _processors = [
        ImageProcessor('APIC', {
            PictureType.OTHER: Image.OTHER,
            PictureType.FRONT_COVER: Image.FRONT_COVER,
            PictureType.BACK_COVER: Image.BACK_COVER,
        }),
        PairProcessor('TMCL', 'guest_performers', {}),
        PairProcessor('TIPL', 'contributors', {
            'producer': 'producer',
            'mix': 'mixer'
        }),
        MultiValueNumericProcessor('TRCK', 'track_number', 'total_tracks')
    ]

    for key, tag in {'TCMP': 'compilation'}.items():
        _processors.append(BooleanProcessor(key, tag))

    for key, tag in {'TALB': 'release_name',
                     'TPE1': 'lead_performer',
                     'TOWN': 'label_name',
                     'TDRC': 'recording_time',
                     'TDRL': 'release_time',
                     'TDOR': 'original_release_time',
                     'TIT2': 'track_title',
                     'TPE4': 'versionInfo',
                     'TEXT': 'lyricist',
                     'TCOM': 'composer',
                     'TPUB': 'publisher',
                     'TSRC': 'isrc',
                     'TLAN': 'language',
                     'TXXX:Catalog Number': 'catalog_number',
                     'TXXX:BARCODE': 'upc',
                     'TXXX:Recording Studios': 'recording_studios',
                     'TXXX:Featured Guest': 'featuredGuest',
                     'TXXX:Tags': 'labels',
                     'TXXX:TAGGER': 'tagger',
                     'TXXX:TAGGER_VERSION': 'tagger_version',
                     'TXXX:TAGGING_TIME': 'tagging_time',
                     'TXXX:ISNI': 'isni',
                     "TXXX:ISWC": "iswc",
                     "COMM::fra": 'comments',
                     "USLT::fra": 'lyrics',
                     'TCON': 'primary_style'
    }.items():
        _processors.append(UnicodeProcessor(key, tag))

    _all_processors = _upgraders + _processors

    def __init__(self, encoding=UTF_8, overwrite=False):
        self._encoding = encoding
        self._overwrite = overwrite

    def load(self, filename):
        audioFile = mp3.MP3(filename)

        frames = audioFile.tags or {}

        metadata = Metadata()
        metadata['duration'] = audioFile.info.length
        metadata['bitrate'] = audioFile.info.bitrate

        for processor in self._all_processors:
            processor.processFrames(metadata, frames)

        return metadata

    def save(self, filename, metadata):
        frames = self._loadFrames(filename)
        if self._overwrite:
            frames.clear()

        for processor in self._all_processors:
            processor.processMetadata(frames, self._encoding, metadata)

        frames.save(filename)

    def _loadFrames(self, filename):
        try:
            return id3.ID3(filename)
        except id3.ID3NoHeaderError:
            return id3.ID3()
