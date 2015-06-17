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

from hamcrest import has_properties, has_entries
import pytest

from cute.finders import WidgetIdentity
from cute.probes import ValueMatcherProbe
from test.drivers.new_album_screen_driver import NewAlbumPageDriver
from test.util import resources
from tgit.album import Album
from tgit.ui.new_album_page import NewAlbumPage


@pytest.fixture()
def on_select(tmpdir):
    def on_select_callback(callback):
        callback(tmpdir.strpath)

    return on_select_callback


@pytest.fixture()
def page(main_window, on_select):
    new_album_screen = NewAlbumPage(select_album_destination=on_select, select_track_location=on_select)
    main_window.setCentralWidget(new_album_screen)
    return new_album_screen


@pytest.yield_fixture()
def driver(page, prober, automaton):
    page_driver = NewAlbumPageDriver(WidgetIdentity(page), prober, automaton)
    yield page_driver
    page_driver.close()


def test_signals_album_creation(page, driver, tmpdir):
    destination = tmpdir.strpath
    page.set_type(Album.Type.FLAC)

    create_album_signal = ValueMatcherProbe("new album properties",
                                            has_entries(album_name="Honeycomb", album_location=destination,
                                                        type=Album.Type.FLAC))
    page.on_create_album(create_album_signal.received)

    driver.create_empty_album("Honeycomb", destination)
    driver.check(create_album_signal)


def test_signals_album_creation_using_shortcut(page, driver, tmpdir):
    destination = tmpdir.strpath
    page.set_type(Album.Type.FLAC)

    create_album_signal = ValueMatcherProbe("new album properties",
                                            has_entries(album_name="Honeycomb", album_location=destination,
                                                        type=Album.Type.FLAC))
    page.on_create_album(create_album_signal.received)

    driver.create_empty_album("Honeycomb", destination, using_shortcut=True)
    driver.check(create_album_signal)


def test_signals_album_import(page, driver, tmpdir):
    destination = tmpdir.strpath
    track_location = resources.path("base.mp3")
    page.set_type(Album.Type.FLAC)

    import_album_signal = ValueMatcherProbe("new album properties",
                                            has_entries(album_name="Honeycomb", album_location=destination,
                                                        type=Album.Type.FLAC, track_location=track_location))
    page.on_import_album(import_album_signal.received)

    driver.import_album("Honeycomb", destination, track_location)
    driver.check(import_album_signal)


def test_signals_album_creation_cancellation(page, driver):
    cancel_creation_signal = ValueMatcherProbe("cancel creation")
    page.on_cancel_creation(lambda: cancel_creation_signal.received())

    driver.cancel_creation()
    driver.check(cancel_creation_signal)


def test_signals_album_creation_cancellation_using_shortcut(page, driver):
    cancel_creation_signal = ValueMatcherProbe("cancel creation")
    page.on_cancel_creation(lambda: cancel_creation_signal.received())

    driver.cancel_creation(using_shortcut=True)
    driver.check(cancel_creation_signal)


def test_selects_an_album_location(driver, tmpdir):
    driver.select_album()
    driver.has_album_location(tmpdir.strpath)


def test_selects_reference_track_location(driver, tmpdir):
    driver.select_track()
    driver.has_track_location(tmpdir.strpath)


def test_initially_disables_create_button(driver):
    driver.creation_is_disabled()
