# -*- coding: utf-8 -*-
from hamcrest import assert_that, contains, has_properties, equal_to

from tgit.identity import Identity


def test_creates_identity():
    identity = Identity(firstName="the first name",
                        lastName="the last name",
                        mainName="the main name",
                        dateOfBirth="1968",
                        dateOfDeath="1998",
                        type="the type",
                        id="0000112345",
                        works=[{"title": "the title", "subtitle": "the subtitle"}])

    assert_that(identity,
                has_properties(first_name="the first name",
                               last_name="the last name",
                               main_name="the main name",
                               date_of_birth="1968",
                               date_of_death="1998",
                               type="the type",
                               id="0000112345",
                               works=contains(has_properties(title="the title", subtitle="the subtitle"))))


def test_fullname_concatenates_first_and_last_name_for_individuals():
    identity = Identity(id="...", type="individual", firstName="Rebecca Ann", lastName="Maloy", works=[])
    assert_that(identity.full_name, equal_to("Rebecca Ann Maloy"), "The full name")


def test_fullname_return_main_name_for_organisations():
    identity = Identity(id="...", type="organisation", mainName="The beatles", works=[])
    assert_that(identity.full_name, equal_to("The beatles"), "The full name")


def test_returns_the_longest_work_title():
    identity = Identity(id="...", type="individual",
                        works=[{"title": "title 1"},
                               {"title": "title 12", "subtitle": "with subtitle"}])

    assert_that(identity.longest_title, equal_to("title 12 with subtitle"))


def test_returns_empty_string_when_works_is_empty():
    identity = Identity(id="...", type="individual", works=[])
    assert_that(identity.longest_title, equal_to(""))
