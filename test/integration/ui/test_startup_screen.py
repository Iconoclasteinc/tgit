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
from test.drivers.startup_screen_driver import StartupScreenDriver
from test.util import resources
from tgit.album import Album
from tgit.ui import StartupScreen
from tgit.ui.new_album_page import NewAlbumPage
from tgit.ui.welcome_page import WelcomePage


@pytest.fixture()
def screen(main_window):
    def create_welcome_page():
        return WelcomePage(select_album=lambda: None)

    def create_new_album_page():
        return NewAlbumPage(select_album_destination=lambda: None, select_track_location=lambda: None)

    startup_screen = StartupScreen(create_welcome_page=create_welcome_page,
                                   create_new_album_page=create_new_album_page)
    main_window.setCentralWidget(startup_screen)
    return startup_screen


@pytest.yield_fixture()
def driver(screen, prober, automaton):
    wizard_driver = StartupScreenDriver(WidgetIdentity(screen), prober, automaton)
    yield wizard_driver
    wizard_driver.close()


def test_initially_shows_the_welcome_page(driver):
    driver.shows_welcome_page()


def test_navigates_to_new_album_page_when_creating_mp3_album(driver):
    driver.creates_album(of_type=Album.Type.MP3)


def test_navigates_to_new_album_page_when_creating_flac_album(driver):
    driver.creates_album(of_type=Album.Type.FLAC)


def test_navigates_to_welcome_page_when_cancelling_the_creation(driver):
    driver.cancels_creation()
