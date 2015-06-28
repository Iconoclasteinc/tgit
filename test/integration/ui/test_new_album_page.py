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

from cute.finders import WidgetIdentity
from cute.probes import ValueMatcherProbe
from test.drivers.new_album_page_driver import NewAlbumPageDriver
from test.util import resources
from tgit.ui import message_box
from tgit.ui.new_album_page import NewAlbumPage
from tgit.util import fs


@pytest.fixture()
def on_select(tmpdir):
    def on_select_callback(callback):
        callback(tmpdir.strpath)

    return on_select_callback


@pytest.fixture()
def page(on_select, qt):
    new_album_page = NewAlbumPage(select_album_destination=on_select,
                                    select_track_location=on_select,
                                    confirm_overwrite=message_box.overwrite_confirmation_message)
    new_album_page.show()
    return new_album_page


@pytest.yield_fixture()
def driver(page, prober, automaton):
    page_driver = NewAlbumPageDriver(WidgetIdentity(page), prober, automaton)
    yield page_driver
    page_driver.close()


@pytest.mark.parametrize("using_shortcut", [False, True])
def test_signals_album_creation(page, driver, tmpdir, using_shortcut):
    create_album_signal = ValueMatcherProbe("new album",
                                            ("flac", tmpdir.join("Honeycomb", "Honeycomb.tgit").strpath))

    page.on_create_album(lambda *args: create_album_signal.received(args))

    driver.create_album("flac", "Honeycomb", tmpdir.strpath, using_shortcut=using_shortcut)
    driver.check(create_album_signal)


def test_signals_album_import(page, driver, tmpdir):
    track_location = resources.path("base.mp3")

    import_album_signal = ValueMatcherProbe("import album",
                                            ("mp3", tmpdir.join("Honeycomb", "Honeycomb.tgit").strpath, track_location))
    page.on_import_album(lambda *args: import_album_signal.received(args))

    driver.create_album("mp3", "Honeycomb", tmpdir.strpath, import_from=track_location)
    driver.check(import_album_signal)


@pytest.mark.parametrize("using_shortcut", [False, True])
def test_signals_album_creation_cancellation(page, driver, tmpdir, using_shortcut):
    cancel_creation_signal = ValueMatcherProbe("cancel creation")
    page.on_cancel_creation(lambda: cancel_creation_signal.received())

    driver.cancel_creation("mp3", "Honeycomb", tmpdir.strpath, using_shortcut=using_shortcut)
    driver.check(cancel_creation_signal)


def test_selects_an_album_location(driver, tmpdir):
    driver.select_album()
    driver.has_album_location(tmpdir.strpath)


def test_selects_reference_track_location(driver, tmpdir):
    driver.select_track()
    driver.has_track_location(tmpdir.strpath)


def test_disables_create_button_when_album_name_or_location_missing(driver):
    driver.enter_album_name("")
    driver.creation_is_disabled()
    driver.enter_album_name("Honeycomb")
    driver.enter_album_location("")
    driver.creation_is_disabled()


def test_resets_form(page, driver):
    driver.select_album_type("mp3")
    driver.enter_album_name("Honeycomb")
    driver.enter_album_location("/path/to/albums")
    driver.enter_track_location("/path/to/tracks")

    page.reset()

    driver.has_reset_form()


def test_asks_for_confirmation_when_album_file_already_exists(driver, tmpdir):
    album_folder = tmpdir.mkdir("Honeycomb")
    touch(album_folder.join("Honeycomb.tgit"))

    driver.create_album("mp3", "Honeycomb", tmpdir.strpath)
    driver.confirm_overwrite()


def touch(filename):
    fs.write(filename.strpath, b"")
