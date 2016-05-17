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
from datetime import datetime
import os
import uuid

from xml.etree import ElementTree


class FileHeader:
    def __init__(self, filename):
        self._filename = filename

    def write_to(self, root):
        header_element = ElementTree.SubElement(root, "FileHeader")
        file_id_element = ElementTree.SubElement(header_element, "FileId")
        file_id_element.text = str(uuid.uuid4())
        file_created_datetime_element = ElementTree.SubElement(header_element, "FileCreatedDateTime")
        file_created_datetime_element.text = datetime.utcnow().isoformat()
        file_name_element = ElementTree.SubElement(header_element, "FileName")
        file_name_element.text = os.path.basename(self._filename)
