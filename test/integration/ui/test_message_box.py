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
from tgit.ui.message_box import MessageBoxes

DISPLAY_DELAY = 100


@pytest.yield_fixture()
def message_box_driver(prober, automaton):
    driver = QMessageBoxDriver(window(QMessageBox, named("message_box")), prober, automaton)
    yield driver
    driver.close()


@pytest.fixture()
def message_boxes(qt):
    return MessageBoxes()


def test_shows_isni_assignation_failed_message_with_details(message_boxes, message_box_driver):
    _ = message_boxes.warn_isni_assignation_failed(details="Details")
    message_box_driver.is_active()
    message_box_driver.shows_message("Could not assign an ISNI")
    message_box_driver.shows_details("Details")
    message_box_driver.ok()


def test_shows_close_album_message(message_boxes, message_box_driver):
    _ = message_boxes.confirm_close_album()

    message_box_driver.is_active()
    message_box_driver.shows_message("Are you sure you want to stop working on this release?")

def test_shows_restart_message(message_boxes, message_box_driver):
    _ = message_boxes.inform_restart_required()

    message_box_driver.is_active()
    message_box_driver.shows_message("You need to restart TGiT for changes to take effect.")


def test_shows_overwrite_album_confirmation_message(message_boxes, message_box_driver):
    _ = message_boxes.confirm_album_overwrite()

    message_box_driver.is_active()
    message_box_driver.shows_message("This album already exists. Are you sure you want to replace it?")


def test_signals_when_confirmed(message_boxes, message_box_driver):
    accept_signal = ValueMatcherProbe("accept confirmation")
    _ = message_boxes.confirm_close_album(on_accept=accept_signal.received)

    message_box_driver.is_active()
    message_box_driver.pause(DISPLAY_DELAY)
    message_box_driver.yes()
    message_box_driver.check(accept_signal)
