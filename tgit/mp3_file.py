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

from mutagen import mp3, id3

from tgit import tags as tagging
from tgit.metadata import Metadata, Image


def invert(mapping):
    return dict([(v, k) for k, v in mapping.iteritems()])


def load(filename):
    mp3 = MP3File(filename)
    mp3.load()
    return mp3


def save(filename, metadata, overwrite=False):
    mp3 = MP3File(filename)
    mp3.save(metadata=metadata, overwrite=overwrite)
    return mp3


class MP3File(object):
    UTF_8 = 3

    class TextProcessor(object):
        def __init__(self, key, tag):
            self._key = key
            self._tag = tag

        def processFrames(self, metadata, frames):
            if self._key in frames:
                frame = frames[self._key]
                metadata[self._tag] = unicode(frame)

        def processMetadata(self, frames, encoding, metadata):
            if self._tag in metadata:
                id, desc = self._decompose(self._key)
                text = metadata[self._tag]
                frames.add(getattr(id3, id)(encoding=encoding, desc=desc, text=text))

        def _decompose(self, key):
            parts = key.split(':')
            return parts[0], (parts[1] if len(parts) > 1 else None)

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
            count = defaultdict(lambda: 0)

            for image in metadata.images:
                frames.add(self._makePictureFrame(count, encoding, image))

        def _makePictureFrame(self, count, encoding, image):
            description = image.desc
            if count[image.desc] > 0:
                description += " (%i)" % (count[image.desc] + 1)
            count[image.desc] += 1
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

    processors = [
        ImageProcessor('APIC', {
            0: Image.OTHER,
            3: Image.FRONT_COVER,
            4: Image.BACK_COVER,
        }),
        PairProcessor('TMCL', tagging.GUEST_PERFORMERS, {}),
        PairProcessor('TIPL', tagging.CONTRIBUTORS, {
            'producer': tagging.PRODUCER,
            'mix': tagging.MIXER
        })
    ]

    for key, tag in {'TALB': tagging.RELEASE_NAME,
                     'TPE1': tagging.LEAD_PERFORMER,
                     'TOWN': tagging.LABEL_NAME,
                     'TDRC': tagging.RECORDING_TIME,
                     'TDRL': tagging.RELEASE_TIME,
                     'TDOR': tagging.ORIGINAL_RELEASE_TIME,
                     'TIT2': tagging.TRACK_TITLE,
                     'TPE4': tagging.VERSION_INFO,
                     'TEXT': tagging.LYRICIST,
                     'TCOM': tagging.COMPOSER,
                     'TPUB': tagging.PUBLISHER,
                     'TSRC': tagging.ISRC,
                     'TXXX:Catalog Number': tagging.CATALOG_NUMBER,
                     'TXXX:UPC': tagging.UPC,
                     'TXXX:Recording Studios': tagging.RECORDING_STUDIOS,
                     'TXXX:Featured Guest': tagging.FEATURED_GUEST, }.items():
        processors.append(TextProcessor(key, tag))

    def __init__(self, filename):
        super(MP3File, self).__init__()
        self._filename = filename
        self._metadata = Metadata()

    @property
    def filename(self):
        return self._filename

    @property
    def metadata(self):
        return self._metadata

    def load(self):
        audioFile = mp3.MP3(self._filename)

        frames = audioFile.tags or {}

        for processor in self.processors:
            processor.processFrames(self._metadata, frames)

        self._metadata[tagging.DURATION] = audioFile.info.length
        self._metadata[tagging.BITRATE] = audioFile.info.bitrate

        return self._metadata

    def save(self, metadata=None, encoding=UTF_8, overwrite=False, filename=None):
        if filename is None:
            filename = self._filename
        if metadata is None:
            metadata = self._metadata

        frames = self._loadFrames(filename)
        if overwrite:
            frames.clear()

        for processor in self.processors:
            processor.processMetadata(frames, encoding, metadata)

        frames.save(filename)

    def _loadFrames(self, filename):
        try:
            return id3.ID3(filename)
        except id3.ID3NoHeaderError:
            return id3.ID3()