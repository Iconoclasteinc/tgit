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

import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers.new_album_page_driver import NewProjectPageDriver
from tgit.ui.pages.new_album_page import NewProjectPage, make_new_project_page


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    page_driver = NewProjectPageDriver(window(NewProjectPage, named("new_project_page")), prober, automaton)
    yield page_driver
    page_driver.close()


def ignore(*_, **__):
    pass


def always(on_accept):
    on_accept()


def no(*_):
    return False


def yes(*_):
    return True


def show_page(of_type="mp3", select_album=ignore, select_track=ignore, confirm_overwrite=always, album_exists=no,
              on_create_project=ignore):
    page = make_new_project_page(select_location=select_album,
                                 select_track=select_track,
                                 confirm_overwrite=confirm_overwrite,
                                 check_project_exists=album_exists,
                                 on_create_project=on_create_project)
    page.project_type = of_type
    page.show()
    return page


@pytest.mark.parametrize("using_shortcut", [False, True])
def test_signals_album_creation(driver, using_shortcut):
    show_page(of_type="flac", on_create_project=lambda *args: create_album_signal.received(args))
    create_album_signal = ValueMatcherProbe("new album", ("flac", "Honeycomb", "~Documents", "track.mp3"))

    driver.create_project("Honeycomb", "~Documents", import_from="track.mp3", using_shortcut=using_shortcut)
    driver.check(create_album_signal)


@pytest.mark.parametrize("using_shortcut", [False, True])
def test_signals_album_creation_cancellation(driver, using_shortcut):
    cancel_creation_signal = ValueMatcherProbe("cancel creation")
    page = show_page()
    page.on_cancel_creation(lambda: cancel_creation_signal.received())

    driver.cancel_creation("Honeycomb", "~Documents", using_shortcut=using_shortcut)
    driver.check(cancel_creation_signal)


def test_selects_an_album_location(driver):
    show_page(select_album=lambda handler: handler("/path/to/album"))

    driver.select_project()
    driver.has_location("/path/to/album")


def test_selects_reference_track_location(driver):
    show_page(select_track=lambda type_, handler: handler("track." + type_))

    driver.select_track()
    driver.has_reference_track("track.mp3")


def test_disables_create_button_when_album_name_or_location_missing(driver):
    show_page()

    driver.enter_name("")
    driver.creation_is_disabled()
    driver.enter_name("Honeycomb")
    driver.enter_location("")
    driver.creation_is_disabled()


def test_resets_form_on_show(driver):
    page = show_page()

    driver.enter_name("Honeycomb")
    driver.enter_location("~Documents")
    driver.enter_reference_track("~Music/track.mp3")

    page.hide()
    page.show()

    driver.has_reset_form()


def test_asks_for_confirmation_when_album_file_already_exists(driver):
    album_exists_query = ValueMatcherProbe("check album exists", ("Honeycomb", "~Documents"))
    show_page(album_exists=lambda *args: album_exists_query.received(args))

    driver.create_project("Honeycomb", "~Documents")
    driver.check(album_exists_query)


def test_creates_album_if_confirmed(driver):
    create_album_signal = ValueMatcherProbe("new album", ("flac", "Honeycomb", "~Documents", "track.flac"))
    show_page(of_type="flac", album_exists=yes, on_create_project=lambda *args: create_album_signal.received(args))

    driver.create_project("Honeycomb", "~Documents", "track.flac")
    driver.check(create_album_signal)
