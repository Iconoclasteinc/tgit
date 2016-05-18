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
import binascii


class Image(object):
    OTHER = 0
    FRONT_COVER = 1
    BACK_COVER = 2

    def __init__(self, mime, data, type_=OTHER, desc=""):
        self.mime = mime
        self.data = data
        self.type = type_
        self.desc = desc

    def __repr__(self):
        data = binascii.hexlify(self.data[:25] + b".." if len(self.data) > 25 else self.data)
        return "Image(mime={}, type_={}, desc={}, data={}) ({} bytes)".format(self.mime, self.type, self.desc, data,
                                                                              len(self.data))

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Metadata:
    def __init__(self, dict_=None, **meta):
        self._images = []
        self._tags = dict_.copy() if dict_ else {}
        self._tags.update(meta)

    def __getattr__(self, name):
        return self[name]

    def __getitem__(self, key):
        return self._tags.get(key, None)

    def __setitem__(self, key, value):
        self._tags[key] = value

    def __delitem__(self, key):
        del self._tags[key]

    def __contains__(self, key):
        return key in self._tags

    def __len__(self):
        return len(self._tags)

    def __eq__(self, other):
        if type(other) is type(self):
            return self._tags == other._tags and self._images == other._images
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def keys(self):
        return self._tags.keys()

    def items(self):
        return self._tags.items()

    def empty(self):
        return len(self) == 0 and len(self.images) == 0

    @property
    def images(self):
        return list(self._images)

    def images_of_type(self, image_type):
        return [image for image in self._images if image.type == image_type]

    def addImage(self, mime, data, type_=Image.OTHER, desc=""):
        self._images.append(Image(mime, data, type_, desc))

    def add_images(self, *images):
        for image in images:
            self.addImage(image.mime, image.data, image.type, image.desc)

    def remove_images(self):
        del self._images[:]

    def update(self, other):
        self._tags.update(other)
        self._images[:] = other.images
        return self

    def copy(self, *keys):
        if not keys:
            keys = self.keys()

        copy = Metadata({key: self[key] for key in keys if key in self})
        copy.add_images(*self.images)
        return copy

    def clear(self):
        self._tags.clear()
        self.remove_images()

    def get(self, key, default=None):
        return self._tags.get(key, default)

    def __str__(self):
        return str(self._tags) + " with images " + str(self._images)
