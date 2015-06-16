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
from test.drivers.new_album_screen_driver import NewAlbumScreenDriver
from test.util import resources
from tgit.album import Album
from tgit.ui.new_album_screen import NewAlbumScreen


@pytest.fixture()
def screen(main_window):
    new_album_screen = NewAlbumScreen(parent=main_window)
    new_album_screen.show()
    return new_album_screen


@pytest.yield_fixture()
def driver(screen, prober, automaton):
    screen_driver = NewAlbumScreenDriver(WidgetIdentity(screen), prober, automaton)
    yield screen_driver
    screen_driver.close()


def test_signals_album_creation(screen, driver, tmpdir):
    destination = tmpdir.strpath

    create_album_signal = ValueMatcherProbe("new album properties",
                                            has_entries(album_name="Honeycomb", album_location=destination,
                                                        type=Album.Type.FLAC))
    screen.on_create_album(create_album_signal.received)

    driver.create_empty_album("Honeycomb", destination)
    driver.check(create_album_signal)


def test_signals_album_import(screen, driver, tmpdir):
    destination = tmpdir.strpath
    track_location = resources.path("base.mp3")

    import_album_signal = ValueMatcherProbe("new album properties",
                                            has_entries(album_name="Honeycomb", album_location=destination,
                                                        type=Album.Type.FLAC, track_location=track_location))
    screen.on_import_album(import_album_signal.received)

    driver.import_album("Honeycomb", destination, track_location)
    driver.check(import_album_signal)


def test_signals_when_selecting_a_location_for_the_album(screen, driver):
    browse_album_signal = ValueMatcherProbe("selecting album")
    screen.on_select_album_location(lambda pressed: browse_album_signal.received())

    driver.select_album()
    driver.check(browse_album_signal)


def test_signals_when_selecting_the_location_of_the_reference_track(screen, driver):
    browse_track_signal = ValueMatcherProbe("selecting reference track")
    screen.on_select_track_location(lambda pressed: browse_track_signal.received())

    driver.select_track()
    driver.check(browse_track_signal)


def test_changes_the_album_location(screen, driver, tmpdir):
    destination = tmpdir.strpath
    screen.change_album_location(destination)

    driver.has_album_location(destination)


def test_changes_the_reference_track_location(screen, driver, tmpdir):
    destination = tmpdir.join("base.mp3").strpath
    screen.change_track_location(destination)

    driver.has_track_location(destination)
