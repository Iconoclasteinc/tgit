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

from xml.etree import ElementTree

from tgit.export.ddex.rin.file_header import FileHeader
from tgit.export.ddex.rin.musical_work import MusicalWorkList
from tgit.export.ddex.rin.party import PartyList
from tgit.export.ddex.rin.resource import ResourceList


class RinFormat:
    def to_xml(self, project, destination):
        root = self._build_header()
        FileHeader(destination).write_to(root)

        party_list = PartyList.from_(project)
        party_list.write_to(root)

        musical_work_list = MusicalWorkList.from_(project, party_list)
        musical_work_list.write_to(root)

        resource_list = ResourceList.from_(project, party_list, musical_work_list)
        resource_list.write_to(root)
        return root

    @staticmethod
    def _build_header():
        root = ElementTree.Element("rin:RecordingInformationNotification")
        root.attrib["xmlns:rin"] = "http://ddex.net/xml/rin/10"
        root.attrib["xmlns:avs"] = "http://ddex.net/xml/avs/avs"
        root.attrib["xmlns:ds"] = "http://www.w3.org/2000/09/xmldsig#"
        root.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
        root.attrib["xsi:schemaLocation"] = "http://ddex.net/xml/rin/10 file:recording-information-notification.xsd"
        root.attrib["SchemaVersionId"] = "rin/10"
        root.attrib["LanguageAndScriptCode"] = "en"
        return root
