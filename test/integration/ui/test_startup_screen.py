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
from test.integration.ui import show_widget
from tgit.ui.pages.new_project_page import NewProjectPage
from tgit.ui.pages.startup_screen import StartupScreen
from tgit.ui.pages.welcome_page import WelcomePage

ignore = lambda: None
no = lambda _: False


@pytest.fixture()
def screen(qt):
    def create_welcome_page():
        return WelcomePage(select_project=ignore, show_load_error=ignore)

    def create_new_project_page():
        return NewProjectPage(select_location=ignore, select_track=ignore, check_project_exists=no,
                              confirm_overwrite=ignore)

    startup_screen = StartupScreen(create_welcome_page=create_welcome_page,
                                   create_new_project_page=create_new_project_page)
    show_widget(startup_screen)
    return startup_screen


@pytest.yield_fixture()
def driver(screen, prober, automaton):
    wizard_driver = StartupScreenDriver(WidgetIdentity(screen), prober, automaton)
    yield wizard_driver
    wizard_driver.close()


def test_initially_shows_the_welcome_page(driver):
    driver.shows_welcome_page()


def test_opens_new_project_page_to_create_a_project(driver):
    driver.create_project()


def test_returns_to_welcome_page_after_cancelling_project_creation(driver):
    driver.cancel_creation()
