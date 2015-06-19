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

import os
import re
import shutil
import tempfile
import mimetypes


def binary_content_of(filename):
    return open(filename, 'rb').read()


def guess_mime_type(filename):
    return mimetypes.guess_type(filename)[0]


def make_temp_copy(filename, dirname=None):
    _, ext = os.path.splitext(filename)
    copy, path = tempfile.mkstemp(suffix=ext, dir=dirname)
    shutil.copy(filename, path)
    os.close(copy)
    return path


def sanitize(filename):
    return re.sub(r'[/<>?*\\:|"]', '_', filename).strip()


WITHOUT_LEADING_DOT = slice(1, None)


def extension(filename):
    _, ext = os.path.splitext(filename)
    return ext[WITHOUT_LEADING_DOT]


def copy(source_file, destination_file):
    if source_file != destination_file:
        shutil.copy(source_file, destination_file)
