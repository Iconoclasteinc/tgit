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


class Image(object):
    OTHER = 0
    FRONT_COVER = 1
    BACK_COVER = 2

    def __init__(self, mime, data, type_=OTHER, desc=''):
        self.mime = mime
        self.data = data
        self.type = type_
        self.desc = desc

    def __repr__(self):
        data = repr((self.data[:25] + '..') if len(self.data) > 25 else self.data)
        return 'Image(mime=%s, type_=%s, desc=%s, data=%s)' % (self.mime, self.type, self.desc,
                                                               data)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Metadata(object):
    def __init__(self, **metadata):
        self._images = []
        self._tags = dict(**metadata)

    def __getitem__(self, key):
        return self._tags.get(key, '')

    def __setitem__(self, key, value):
        self._tags[key] = value

    def __delitem__(self, key):
        del self._tags[key]

    def __contains__(self, key):
        return key in self._tags

    def __len__(self):
        return len(self._tags)

    def keys(self):
        return self._tags.keys()

    def items(self):
        return self._tags.items()

    @property
    def images(self):
        return list(self._images)

    def imagesOfType(self, imageType):
        return [image for image in self._images if image.type == imageType]

    def addImage(self, mime, data, type_=Image.OTHER, desc=''):
        self._images.append(Image(mime, data, type_, desc))

    def addImages(self, *images):
        for image in images:
            self.addImage(image.mime, image.data, image.type, image.desc)

    def removeImages(self):
        del self._images[:]

    def update(self, other):
        self._tags.update(other._tags)
        self._images[:] = other.images

    def copy(self):
        return self.select(*self._tags.keys())

    def select(self, *keys):
        metadata = Metadata()
        for key in keys:
            metadata[key] = self[key]

        metadata.addImages(*self.images)
        return metadata

    def clear(self):
        self._tags.clear()
        self.removeImages()

    def __str__(self):
        return str(self._tags)