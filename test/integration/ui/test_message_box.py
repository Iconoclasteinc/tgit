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

from PyQt5.QtWidgets import QMainWindow
import pytest

from cute.finders import WidgetIdentity
from cute.prober import EventProcessingProber
from cute.robot import Robot
from cute.widgets import QMessageBoxDriver
from test.integration.ui import show_widget
from tgit.ui import isni_assignation_failed_message_box
from tgit.ui.message_box import close_album_confirmation_box


@pytest.yield_fixture()
def window(qt):
    main_window = QMainWindow()
    show_widget(main_window)
    yield main_window
    main_window.close()


def test_shows_isni_assignation_failed_message_with_details(window):
    dialog = isni_assignation_failed_message_box(window, "Details")
    driver = QMessageBoxDriver(WidgetIdentity(dialog), EventProcessingProber(), Robot())
    dialog.open()

    driver.shows_message("Could not assign an ISNI")
    driver.shows_details("Details")
    driver.ok()


def test_shows_close_album_message(window):
    dialog = close_album_confirmation_box(window)
    driver = QMessageBoxDriver(WidgetIdentity(dialog), EventProcessingProber(), Robot())
    dialog.open()

    driver.shows_message("Are you sure you want to stop working on this release?")
    driver.yes()