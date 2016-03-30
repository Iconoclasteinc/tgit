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
from tgit.cheddar import PlatformConnectionError, PermissionDeniedError, InsufficientInformationError
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


class Identities:
    def __init__(self, total_count, identity_cards):
        self.identity_cards = identity_cards
        self.total_count = total_count

    def __len__(self):
        return len(self.identity_cards)

    def __iter__(self):
        return self.identity_cards.__iter__()

    def overflows(self):
        return int(self.total_count) > len(self.identity_cards)


class IdentitySelection(metaclass=Observable):
    on_identities_available = signal(Identities)
    on_failure = signal(Exception)
    on_connection_failed = signal()
    on_permission_denied = signal()
    on_success = signal()
    on_lookup_start = signal()
    on_assignation_start = signal()
    on_insufficient_information = signal()

    def __init__(self, project, person):
        self._person = person
        self._project = project

    @property
    def person(self):
        return self._person

    @property
    def works(self):
        return [track.track_title for track in self._project.tracks]

    def lookup_started(self):
        self.on_lookup_start.emit()

    def assignation_started(self):
        self.on_assignation_start.emit()

    def identities_found(self, identities):
        identity_cards = [IdentityCard(**identity) for identity in identities["identities"]]
        self.on_identities_available.emit(Identities(identities["total_count"], identity_cards))

    def failed(self, error):
        if isinstance(error, PlatformConnectionError):
            self.on_connection_failed.emit()

        if isinstance(error, PermissionDeniedError):
            self.on_permission_denied.emit()

        if isinstance(error, InsufficientInformationError):
            self.on_insufficient_information.emit()

        self.on_failure.emit(error)

    def identity_selected(self, identity):
        self._project.add_isni(self._person, identity.id)
        self.on_success.emit()

    def identity_assigned(self, identity):
        self.identity_selected(IdentityCard(**identity))


def launch_lookup(cheddar, session, selection):
    def launch_lookup_for(main_artist):
        lookup = cheddar.get_identities(main_artist, session.current_user.api_key)
        lookup.on_success(selection.identities_found)
        lookup.on_failure(selection.failed)
        selection.lookup_started()
    return launch_lookup_for


def launch_assignation(cheddar, session, selection):
    def launch_assignation_of_type(type_):
        assignation = cheddar.assign_identifier(selection.person, type_, selection.works, session.current_user.api_key)
        assignation.on_success(selection.identity_assigned)
        assignation.on_failure(selection.failed)
        selection.assignation_started()
    return launch_assignation_of_type
