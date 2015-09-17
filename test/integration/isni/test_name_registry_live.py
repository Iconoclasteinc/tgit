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

from hamcrest import assert_that, anything, has_item, contains, equal_to, greater_than
import pytest

from tgit.isni.name_registry import NameRegistry

pytestmark = pytest.mark.live


@pytest.yield_fixture
def platform():
    from test.util import cheddar

    server_thread = cheddar.start("isni.oclc.nl", 80)
    yield cheddar
    cheddar.stop(server_thread)


@pytest.fixture
def production_registry(platform):
    return NameRegistry(host=platform.host(), port=platform.port())


def has_identity(isni=anything(), name=anything(), birth_date=anything(), title=anything()):
    return has_item(contains(isni, contains(name, birth_date, title)))


def test_finds_rebecca_ann_maloy_identity(production_registry):
    _, identities = production_registry.search_by_keywords("maloy", "rebecca", "ann")

    assert_that(identities, has_identity("0000000115677274", "Rebecca Ann Maloy"))


def test_finds_only_one_record_when_searching_for_rebecca_ann_maloy_indentity(production_registry):
    number_of_results, _ = production_registry.search_by_keywords("maloy", "rebecca", "ann")

    assert_that(number_of_results, equal_to("1"))


def test_finds_rebecca_ann_maloy_indentity_using_part_of_her_name(production_registry):
    _, identities = production_registry.search_by_keywords("malo", "reb", "a")

    assert_that(identities, has_identity("0000000115677274", "Rebecca Ann Maloy"))


def test_finds_joel_miller_indentity_with_dates(production_registry):
    _, identities = production_registry.search_by_keywords("miller", "joel")

    assert_that(identities, has_identity("0000000073759369", "Joel Miller", "1969-"))


def test_finds_more_than_twenty_matches_when_searching_for_jo_miller(production_registry):
    number_of_records, _ = production_registry.search_by_keywords("Miller", "Jo")

    assert_that(int(number_of_records), greater_than(20))


def test_finds_metallica_identity(production_registry):
    _, identities = production_registry.search_by_keywords("Metallica")

    assert_that(identities, has_identity("0000000122939631", "Metallica"))


def test_finds_the_beatles_identity(production_registry):
    _, identities = production_registry.search_by_keywords("Beatles", "The")

    assert_that(identities, has_identity("0000000121707484", "The Beatles"))


def test_finds_the_beatles_identity_with_prefix_sent_first(production_registry):
    _, identities = production_registry.search_by_keywords("The", "Beatles")

    title = "The fool on the hill from The Beatles' T.V. film Magical mystery tour"
    assert_that(identities, has_identity("0000000121707484", "The Beatles", title=title))


def test_finds_led_zeppelin_identity(production_registry):
    _, identities = production_registry.search_by_keywords("Led", "Zeppelin")

    assert_that(identities, has_identity("0000000123483226", "Led Zeppelin"))


def test_finds_led_zeppelin_identity_with_prefix_sent_first(production_registry):
    _, identities = production_registry.search_by_keywords("Zeppelin", "Led")

    assert_that(identities, has_identity("0000000123483226", "Led Zeppelin"))


def test_finds_rage_against_the_machine_identity(production_registry):
    _, identities = production_registry.search_by_keywords("Rage", "Against", "The", "Machine")

    assert_that(identities, has_identity("0000000122905407", "Rage against the machine"))


def test_finds_rage_against_the_machine_with_prefix_sent_first(production_registry):
    _, identities = production_registry.search_by_keywords("Machine", "Rage", "Against", "The")

    assert_that(identities, has_identity("0000000122905407", "Rage against the machine"))
