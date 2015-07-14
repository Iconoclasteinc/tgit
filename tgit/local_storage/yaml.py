# -*- coding: utf-8 -*-
#
# TGiT, Music Tagger for Professionals
# Copyright (C) 2013 Iconoclaste Musique Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.qp6
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
import yaml


def write_data(filename, album_data):
    with open(filename, "w", encoding="utf-8") as album_file:
        yaml.dump(album_data, stream=album_file, Dumper=yaml.Dumper, default_flow_style=False, allow_unicode=True)


def read_data(filename):
    with open(filename, "r", encoding="utf-8") as album_file:
        data = yaml.load(album_file)

    return data
