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

from PyQt5.QtCore import Qt, QFile, QIODevice
from PyQt5.QtGui import QPixmap, QImage


def scale(image_to_scale, width, height):
    image = _empty() if image_to_scale is None else QImage.fromData(image_to_scale.data)
    if image.byteCount() == 0:
        image = _not_found()

    return QPixmap.fromImage(image.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation))


def _not_found():
    return QImage.fromData(_from_resources(":/images/invalid-image-placeholder.png"))


def _empty():
    return QImage.fromData(_from_resources(":/images/no-image-placeholder.png"))


def _from_resources(path):
    file = QFile(path)
    file.open(QIODevice.ReadOnly)
    bytes_ = file.readAll()
    file.close()
    return bytes_
