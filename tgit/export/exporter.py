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

from tgit.export import soproq_format
from tgit.export.csv_format import CsvFormat


def as_soproq_using(load_workbook, show_confirmation_message, formatter=soproq_format):
    def as_soproq(album, filename):
        workbook = load_workbook()
        formatter.write(album, workbook)
        workbook.save(filename)
        show_confirmation_message()

    return as_soproq


def as_csv(album, destination):
    with open(destination, "w", encoding="windows-1252") as out:
        CsvFormat().write(album, out)
