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
from xml.etree.ElementTree import ElementTree

from tgit.export import soproq_format
from tgit.export.csv_format import CsvFormat
from tgit.export import ddex
from tgit.signal import signal


class ExportLocationSelection:
    on_failure = signal(Exception)

    extensions = ["xml"]

    def __init__(self, project, preferences):
        self._preferences = preferences
        self._project = project

    @property
    def directory(self):
        return self._preferences.export_location

    @property
    def default_file_name(self):
        return "{}.xml".format(self._project.release_name)

    def directory_changed(self, directory):
        self._preferences.export_location = directory

    def failed(self, error):
        self.on_failure.emit(error)


def as_soproq_using(load_workbook, show_confirmation_message, formatter=soproq_format):
    def as_soproq(project, filename):
        workbook = load_workbook()
        formatter.write(project, workbook)
        workbook.save(filename)
        show_confirmation_message()

    return as_soproq


def as_csv(project, destination):
    with open(destination, "w", encoding="windows-1252") as out:
        CsvFormat().write(project, out)


def as_ddex_rin(project, export_location_selection):
    def write(root, destination):
        ElementTree(root).write(destination, xml_declaration=True, encoding="UTF-8")

    def export(destination):
        try:
            write(ddex.RinFormat().to_xml(project, destination), destination)
        except Exception as e:
            export_location_selection.failed(e)

    return export
