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

from tgit.export.ddex.rin.section import Section


class FileHeader(Section):
    def __init__(self, filename):
        self._filename = filename

    def write_to(self, root):
        header = self._build_sub_element(root, "FileHeader")
        self._build_sub_element(header, "FileId", str(uuid.uuid4()))
        self._build_sub_element(header, "FileCreatedDateTime", datetime.utcnow().isoformat())
        self._build_sub_element(header, "FileName", os.path.basename(self._filename))
