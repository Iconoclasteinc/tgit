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
from hamcrest import contains_string
import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import QMessageBoxDriver, window
from test.drivers.about_dialog_driver import AboutDialogDriver
from tgit import platforms
from tgit.ui import AboutDialog
from tgit.ui.message_boxes import MessageBoxes

DISPLAY_DELAY = 200 if platforms.mac else 0


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    message_box_driver = QMessageBoxDriver(window(QMessageBox, named("message_box")), prober, automaton)
    yield message_box_driver
    message_box_driver.close()


@pytest.yield_fixture()
def about_tgit_driver(qt, prober, automaton):
    message_box_driver = AboutDialogDriver(window(AboutDialog, named("about_tgit_dialog")), prober, automaton)
    yield message_box_driver
    message_box_driver.close()


def messages():
    return MessageBoxes()


def test_shows_isni_assignation_failed_message_with_details(driver):
    _ = messages().isni_assignation_failed(details="Details")
    driver.is_active()
    driver.shows_message("Could not assign an ISNI")
    driver.shows_details("Details")
    driver.ok()


def test_shows_close_album_message(driver):
    _ = messages().close_album_confirmation()

    driver.is_active()
    driver.shows_message(contains_string("You are about to close the current album."))


def test_shows_restart_message(driver):
    _ = messages().restart_required()

    driver.is_active()
    driver.shows_message(contains_string("You need to restart TGiT for changes to take effect."))


def test_shows_overwrite_album_confirmation_message(driver):
    _ = messages().overwrite_album_confirmation()

    driver.is_active()
    driver.shows_message(contains_string("This album already exists."))


def test_signals_when_confirmed(driver):
    accept_signal = ValueMatcherProbe("accept confirmation")
    _ = messages().close_album_confirmation(on_accept=accept_signal.received)

    driver.is_active()
    driver.pause(DISPLAY_DELAY)
    driver.yes()
    driver.check(accept_signal)


def test_shows_load_album_failed_message(driver):
    _ = messages().load_album_failed(Exception())

    driver.is_active()
    driver.shows_message(contains_string("The album file you selected cannot be loaded."))


def test_shows_save_album_failed_message(driver):
    _ = messages().save_album_failed(Exception())

    driver.is_active()
    driver.shows_message(contains_string("Your album file could not be saved."))


def test_shows_export_failed_message(driver):
    _ = messages().export_failed(Exception())

    driver.is_active()
    driver.shows_message("Could not export your album.")


def test_shows_about_message(about_tgit_driver):
    _ = messages().about_tgit()

    about_tgit_driver.is_active()
