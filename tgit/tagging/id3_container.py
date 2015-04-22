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


def invert(mapping):
    return dict(list(zip(list(mapping.values()), list(mapping.keys()))))


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
        frame, desc, lang = self._decompose(self._key)
        text = metadata[self._tag]
        frames.delall(self._key)
        if text:
            frames.add(getattr(id3, frame)(encoding=encoding, desc=desc, lang=lang, text=self._toFrame(text)))

    def _decompose(self, key):
        parts = (key + '::').split(':')
        return parts[0], parts[1], parts[2]


class UnicodeProcessor(TextProcessor):
    def __init__(self, key, tag):
        super(UnicodeProcessor, self).__init__(key, tag, str, str)


class BooleanProcessor(TextProcessor):
    @staticmethod
    def toBoolean(text):
        return text == '1'

    @staticmethod
    def toText(boolean):
        return boolean and '1' or '0'

    def __init__(self, key, tag):
        super(BooleanProcessor, self).__init__(key, tag, self.toBoolean, self.toText)


class ImageProcessor(object):
    def __init__(self, key, pictureTypes):
        self._key = key
        self._pictureTypes = pictureTypes

    def processFrames(self, metadata, frames):
        for key in self._pictureFrames(frames):
            picture = frames[key]
            imageType = self._pictureTypes.get(picture.type, Image.OTHER)
            metadata.addImage(picture.mime, picture.data, imageType, picture.desc)

    def _pictureFrames(self, frames):
        return [key for key in frames if key.startswith(self._key)]

    def processMetadata(self, frames, encoding, metadata):
        frames.delall(self._key)
        count = Counter()
        for image in metadata.images:
            count[image.desc] += 1
            frames.add(self._makePictureFrame(count, encoding, image))

    def _makePictureFrame(self, count, encoding, image):
        description = image.desc
        if count[image.desc] > 1:
            description += ' ({})'.format(count[image.desc])

        imagesTypes = invert(self._pictureTypes)
        return getattr(id3, self._key)(encoding=encoding, mime=image.mime,
                                       type=imagesTypes[image.type],
                                       desc=description, data=image.data)


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
        if not self._tag in metadata:
            return []
        return [[role, name] for role, name in metadata[self._tag]]


class ID3Container(object):
    UTF_8 = 3

    def __init__(self, encoding=UTF_8, overwrite=False):
        self._encoding = encoding
        self._overwrite = overwrite

    processors = [
        ImageProcessor('APIC', {
            0: Image.OTHER,
            3: Image.FRONT_COVER,
            4: Image.BACK_COVER,
        }),
        PairProcessor('TMCL', 'guestPerformers', {}),
        PairProcessor('TIPL', 'contributors', {
            'producer': 'producer',
            'mix': 'mixer'
        })
    ]

    for key, tag in {'TALB': 'release_name',
                     'TPE1': 'lead_performer',
                     'TOWN': 'labelName',
                     'TDRC': 'recordingTime',
                     'TDRL': 'releaseTime',
                     'TDOR': 'originalReleaseTime',
                     'TIT2': 'track_title',
                     'TPE4': 'versionInfo',
                     'TEXT': 'lyricist',
                     'TCOM': 'composer',
                     'TPUB': 'publisher',
                     'TSRC': 'isrc',
                     'TLAN': 'language',
                     'TXXX:Catalog Number': 'catalogNumber',
                     'TXXX:UPC': 'upc',
                     'TXXX:Recording Studios': 'recordingStudios',
                     'TXXX:Featured Guest': 'featuredGuest',
                     'TXXX:Tags': 'labels',
                     'TXXX:Tagger': 'tagger',
                     'TXXX:Tagging Time': 'taggingTime',
                     'TXXX:ISNI': 'isni',
                     "COMM::fra": 'comments',
                     "USLT::fra": 'lyrics',
                     'TCON': 'primaryStyle'
    }.items():
        processors.append(UnicodeProcessor(key, tag))

    for key, tag in {'TCMP': 'compilation'}.items():
        processors.append(BooleanProcessor(key, tag))

    def load(self, filename):
        audioFile = mp3.MP3(filename)

        frames = audioFile.tags or {}

        metadata = Metadata()
        for processor in self.processors:
            processor.processFrames(metadata, frames)

        metadata['duration'] = audioFile.info.length
        metadata['bitrate'] = audioFile.info.bitrate

        return metadata

    def save(self, filename, metadata):
        frames = self._loadFrames(filename)
        if self._overwrite:
            frames.clear()

        for processor in self.processors:
            processor.processMetadata(frames, self._encoding, metadata)

        frames.save(filename)

    def _loadFrames(self, filename):
        try:
            return id3.ID3(filename)
        except id3.ID3NoHeaderError:
            return id3.ID3()