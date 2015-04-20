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

from hamcrest import assert_that, anything, has_item, contains, equal_to, greater_than

from tgit.isni.name_registry import NameRegistry


def has_identity(isni=anything(), name=anything(), birth_date=anything(), title=anything()):
    return has_item(contains(isni, contains(name, birth_date, title)))


class IsniLiveTest(unittest.TestCase):
    def testFindsRebeccaAnnMaloyIdentity(self):
        registry = NameRegistry(host="isni.oclc.nl")
        _, identities = registry.search_by_keywords("maloy", "rebecca", "ann")

        assert_that(identities, has_identity("0000000115677274", "Rebecca Ann Maloy"))

    def testFindsOnlyOneRecordWhenSearchingForRebeccaAnnMaloyIndentity(self):
        registry = NameRegistry(host="isni.oclc.nl")
        number_of_results, _ = registry.search_by_keywords("maloy", "rebecca", "ann")

        assert_that(number_of_results, equal_to("1"))

    def testFindsRebeccaAnnMaloyIndentityUsingPartOfHerName(self):
        registry = NameRegistry(host="isni.oclc.nl")
        _, identities = registry.search_by_keywords("malo", "reb", "a")

        assert_that(identities, has_identity("0000000115677274", "Rebecca Ann Maloy"))

    def testFindsJoelMillerIndentityWithDates(self):
        registry = NameRegistry(host="isni.oclc.nl")
        _, identities = registry.search_by_keywords("miller", "joel")

        assert_that(identities, has_identity("0000000073759369", "Joel Miller", "1969-"))

    def testFindsMoreThanTwentyMatchesWhenSearchingForJoMiller(self):
        registry = NameRegistry(host="isni.oclc.nl")
        number_of_records, _ = registry.search_by_keywords("Miller", "Jo")

        assert_that(int(number_of_records), greater_than(20))

    def testFindsMetallicaIdentity(self):
        registry = NameRegistry(host="isni.oclc.nl")
        _, identities = registry.search_by_keywords("Metallica")

        assert_that(identities, has_identity("0000000122939631", "Metallica"))

    def testFindsTheBeatlesIdentity(self):
        registry = NameRegistry(host="isni.oclc.nl")
        _, identities = registry.search_by_keywords("Beatles", "The")

        assert_that(identities, has_identity("0000000121707484", "The Beatles"))

    def testFindsTheBeatlesIdentityWithPrefixSentFirst(self):
        registry = NameRegistry(host="isni.oclc.nl")
        _, identities = registry.search_by_keywords("The", "Beatles")

        title = "The fool on the hill from The Beatles' T.V. film Magical mystery tour"
        assert_that(identities, has_identity("0000000121707484", "The Beatles", title=title))

    def testFindsLedZeppelinIdentity(self):
        registry = NameRegistry(host="isni.oclc.nl")
        _, identities = registry.search_by_keywords("Led", "Zeppelin")

        assert_that(identities, has_identity("0000000123483226", "Led Zeppelin"))

    def testFindsLedZeppelinIdentityWithPrefixSentFirst(self):
        registry = NameRegistry(host="isni.oclc.nl")
        _, identities = registry.search_by_keywords("Zeppelin", "Led")

        assert_that(identities, has_identity("0000000123483226", "Led Zeppelin"))

    def testFindsRageAgainstTheMachineIdentity(self):
        registry = NameRegistry(host="isni.oclc.nl")
        _, identities = registry.search_by_keywords("Rage", "Against", "The", "Machine")

        assert_that(identities, has_identity("0000000122905407", "Rage against the machine"))

    def testFindsRageAgainstTheMachineWithPrefixSentFirst(self):
        registry = NameRegistry(host="isni.oclc.nl")
        _, identities = registry.search_by_keywords("Machine", "Rage", "Against", "The")

        assert_that(identities, has_identity("0000000122905407", "Rage against the machine"))

    @unittest.skip("ISNI Response changes too often for test to be valid")
    def testAssignAnISNIUsingFullNameAndTitleOfWorks(self):
        registry = NameRegistry(assign_host="isni-m-acc.oclc.nl")
        isni = registry.assign("Jan", "Baerthel", "Industrielles Bauen: Leitfaden", "Industrielles Bauen")

        assert_that(isni, equal_to("0000000124568061"))