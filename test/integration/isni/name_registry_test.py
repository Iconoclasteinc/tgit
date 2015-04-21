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
import unittest

from hamcrest import assert_that, contains, has_item, anything, equal_to
import pytest

from tgit.isni.name_registry import NameRegistry
import test.util.isni_database as server


def has_identity(isni=anything(), name=anything(), birth_date=anything(), title=anything()):
    return has_item(contains(isni, contains(name, birth_date, title)))


class IsniTest(unittest.TestCase):
    def setUp(self):
        server.port = 5000
        self.server_thread = server.start()
        self.registry = NameRegistry(host="localhost", assign_host="localhost", port=server.port)

    def tearDown(self):
        server.persons.clear()
        server.organisations.clear()
        server.assignations = None
        server.stop(self.server_thread)

    def test_finds_person(self):
        server.persons["00000001"] = [{"names": [
            ("Joel", "Miller", "1969-"), ("Joel E.", "Miller", ""), ("joel", "miller", "")], "titles": ["Honeycombs"]}]

        identities = self.registry.search_by_keywords("joel", "miller")
        assert_that(identities[0], equal_to("1"))
        assert_that(identities[1], has_identity("00000001", "Joel E. Miller", "1969-", "Honeycombs"))

    def test_finds_organisation(self):
        server.organisations["0000000121707484"] = [{"names": [
            "The Beatles", "Beatles, The"], "titles": [
            "The fool on the hill from The Beatles' T.V. film Magical mystery tour"]}]

        identities = self.registry.search_by_keywords("The", "Beatles")

        assert_that(identities[0], equal_to("1"))
        assert_that(identities[1],
                    has_identity("0000000121707484", "Beatles, The",
                                 title="The fool on the hill from The Beatles' T.V. film Magical mystery tour"))

    def test_assigns_isni_to_person(self):
        server.assignation_generator = (isni for isni in ["0000000121707484"])
        code, isni = self.registry.assign("Joel", "Miller", ["Zumbar", "Salsa Coltrane", "Big Ideas"])
        assert_that(code, equal_to(NameRegistry.Codes.SUCCESS))
        assert_that(isni, equal_to("0000000121707484"))

    def test_notifies_that_request_was_incomplete_when_assigning_a_person(self):
        server.assignation_generator = (isni for isni in ["sparse"])
        code, message = self.registry.assign("Joel", "Miller", ["Zumbar", "Salsa Coltrane", "Big Ideas"])
        assert_that(code, equal_to(NameRegistry.Codes.SPARSE))
        assert_that(message, equal_to("needs at least one of title, date, instrument, contributedTo"))

    def test_notifies_that_request_was_invalid_when_assigning_a_person(self):
        server.assignation_generator = (isni for isni in ["invalid data"])
        code, message = self.registry.assign("Joel", "Miller", ["Zumbar", "Salsa Coltrane", "Big Ideas"])
        assert_that(code, equal_to(NameRegistry.Codes.INVALID_DATA))
        assert_that(message, equal_to("invalid code creationRole eee"))

    def test_notifies_that_request_was_malformed_when_assigning_a_person(self):
        server.assignation_generator = (isni for isni in [""])
        code, message = self.registry.assign("<Joel>", "<Miller>", ["Zumbar", "Salsa Coltrane", "Big Ideas"])
        assert_that(code, equal_to(NameRegistry.Codes.INVALID_FORMAT))
        assert_that(message, equal_to("XML parsing error"))

    @pytest.mark.wip
    def test_assigns_isni_to_person_from_a_possible_match(self):
        pass

    @pytest.mark.wip
    def test_assigns_isni_to_person_after_having_turned_down_all_possible_matches(self):
        pass