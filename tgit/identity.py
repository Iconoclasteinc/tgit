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


class Work:
    def __init__(self, **kwargs):
        self.title = kwargs["title"]
        self.subtitle = kwargs["subtitle"] if "subtitle" in kwargs else None


class Identity:
    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.type = kwargs["type"]
        self.first_name = kwargs["firstName"] if "firstName" in kwargs else None
        self.last_name = kwargs["lastName"] if "lastName" in kwargs else None
        self.main_name = kwargs["mainName"] if "mainName" in kwargs else None
        self.date_of_birth = kwargs["dateOfBirth"] if "dateOfBirth" in kwargs else None
        self.date_of_death = kwargs["dateOfDeath"] if "dateOfDeath" in kwargs else None
        self.works = [Work(**work) for work in kwargs["works"]]

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name) if self.type == "individual" else self.main_name

    @property
    def longest_title(self):
        return max(
            ["{0} {1}".format(work.title, work.subtitle) if work.subtitle else work.title for work in self.works],
            key=len)
