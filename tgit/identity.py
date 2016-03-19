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
from tgit.signal import signal, Observable


class Work:
    def __init__(self, title, **data):
        self.title = title
        self.subtitle = data.get("subtitle", None)

    @property
    def full_title(self):
        return "{} {}".format(self.title, self.subtitle) if self.subtitle else self.title


class IdentityCard:
    INDIVIDUAL = "individual"
    ORGANIZATION = "organization"

    def __init__(self, **data):
        self.id = data.get("id")
        self.type = data.get("type")
        self.first_name = data.get("firstName", None)
        self.last_name = data.get("lastName", None)
        self.main_name = data.get("mainName", None)
        self.date_of_birth = data.get("dateOfBirth", None)
        self.date_of_death = data.get("dateOfDeath", None)
        self.works = [Work(**work) for work in data.get("works", [])]

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name) if self.type == self.INDIVIDUAL else self.main_name

    @property
    def longest_title(self):
        if len(self.works) == 0:
            return ""

        return max([work.full_title for work in self.works], key=len)


class IdentityLookup(metaclass=Observable):
    on_identities_available = signal(list)
    on_failure = signal(Exception)
    on_success = signal(IdentityCard)
    on_start = signal()

    def lookup_started(self):
        self.on_start.emit()

    def identities_found(self, identities):
        self.on_identities_available.emit([IdentityCard(**identity) for identity in identities])

    def lookup_failed(self, error):
        self.on_failure.emit(error)

    def identity_selected(self, identity):
        self.on_success.emit(identity)


def launch_lookup(cheddar, session, identity_lookup):
    def launch_lookup_for(main_artist):
        lookup = cheddar.get_identities(main_artist, session.current_user.api_key)
        lookup.on_success(identity_lookup.identities_found)
        lookup.on_failure(identity_lookup.lookup_failed)
        identity_lookup.lookup_started()

    return launch_lookup_for
