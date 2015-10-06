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
import unicodedata


def read(filename):
    return open(filename, "rb").read()


def write(filename, data):
    with open(filename, "wb") as file:
        file.write(data)


def guess_mime_type(filename):
    return mimetypes.guess_type(filename)[0]


def guess_extension(mime_type):
    return mimetypes.guess_extension(mime_type)


def make_temp_copy(filename, dirname=None):
    temp_copy, path = tempfile.mkstemp(suffix=ext(filename), dir=dirname)
    copy(filename, path)
    os.close(temp_copy)
    return path


def make_temp_dir():
    return tempfile.mkdtemp(prefix="TGiT_")


def sanitize(filename):
    return re.sub(r'[/<>?*\\:|"]', "_", filename).strip()


def ext(filename):
    _, extension = os.path.splitext(filename)
    return extension


def copy(source_file, destination_file):
    if source_file != destination_file:
        shutil.copy(source_file, destination_file)


def mkdirs(path):
    os.makedirs(path, exist_ok=True)


def normalize(filename):
    return unicodedata.normalize("NFC", filename)


def abspath(path):
    return normalize(os.path.abspath(path))


# todo take a filter argument
def list_dir(folder):
    def full_path(filename):
        return abspath(os.path.join(folder, filename))

    return [full_path(filename) for filename in os.listdir(folder) if os.path.isfile(full_path(filename))]


def remove(path):
    try:
        os.remove(path)
    except OSError:
        pass


_all_files = lambda entry: True


def remove_files(folder, matching=_all_files):
    for filename in list_dir(folder):
        if matching(filename):
            remove(filename)
