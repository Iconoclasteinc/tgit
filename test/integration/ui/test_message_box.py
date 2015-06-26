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
from PyQt5.QtWidgets import QMessageBox
import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import QMessageBoxDriver, window
from tgit.ui import isni_assignation_failed_message_box
from tgit.ui.message_box import close_album_confirmation_box, overwrite_confirmation_message

DISPLAY_DELAY = 100


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    driver = QMessageBoxDriver(window(QMessageBox, named("message_box")), prober, automaton)
    yield driver
    driver.close()


def test_shows_isni_assignation_failed_message_with_details(driver):
    dialog = isni_assignation_failed_message_box(details="Details")
    dialog.open()

    driver.is_active()
    driver.shows_message("Could not assign an ISNI")
    driver.shows_details("Details")
    driver.ok()


def test_shows_close_album_message(driver):
    dialog = close_album_confirmation_box()
    dialog.open()

    driver.is_active()
    driver.shows_message("Are you sure you want to stop working on this release?")


def test_shows_overwrite_album_confirmation_message(driver):
    dialog = overwrite_confirmation_message()
    dialog.open()

    driver.is_active()
    driver.shows_message("This album already exists. Are you sure you want to replace it?")


def test_signals_when_confirmed(driver):
    accept_signal = ValueMatcherProbe("accept confirmation")
    dialog = close_album_confirmation_box(on_accept=accept_signal.received)
    dialog.open()

    driver.is_active()
    driver.pause(DISPLAY_DELAY)
    driver.yes()
    driver.check(accept_signal)
