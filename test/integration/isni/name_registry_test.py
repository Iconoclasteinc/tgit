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

from tgit.isni.name_registry import NameRegistry
import test.util.isni_database as server


def has_identity(isni=anything(), name=anything(), birth_date=anything(), title=anything()):
    return has_item(contains(isni, contains(name, birth_date, title)))


class IsniTest(unittest.TestCase):
    def setUp(self):
        server.port = 5000
        server.start()
        self.registry = NameRegistry(host="localhost", port=server.port)

    def tearDown(self):
        server.persons.clear()
        server.organisations.clear()
        server.stop()

    def testFindsPerson(self):
        server.persons["00000001"] = [{"names": [
            ("Joel", "Miller", "1969-"), ("Joel E.", "Miller", ""), ("joel", "miller", "")], "titles": ["Honeycombs"]}]

        identities = self.registry.search_by_keywords("joel", "miller")
        assert_that(identities[0], equal_to("1"))
        assert_that(identities[1], has_identity("00000001", "Joel E. Miller", "1969-", "Honeycombs"))

    def testFindsOrganisation(self):
        server.organisations["0000000121707484"] = [{"names": [
            "The Beatles", "Beatles, The"], "titles": [
            "The fool on the hill from The Beatles' T.V. film Magical mystery tour"]}]

        identities = self.registry.search_by_keywords("The", "Beatles")

        assert_that(identities[0], equal_to("1"))
        assert_that(identities[1],
                    has_identity("0000000121707484", "Beatles, The",
                                 title="The fool on the hill from The Beatles' T.V. film Magical mystery tour"))