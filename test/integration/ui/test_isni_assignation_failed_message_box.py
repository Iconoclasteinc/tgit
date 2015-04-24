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

from tgit.isni.name_registry import NameRegistry
from test.cute.finders import WidgetIdentity
from test.cute.prober import EventProcessingProber
from test.cute.robot import Robot
from test.drivers.isni_error_message_box_driver import MessageBoxDriver
from test.integration.ui import show_widget
from tgit.ui import isni_assignation_failed_message_box


@pytest.yield_fixture()
def window(qt):
    main_window = QMainWindow()
    show_widget(main_window)
    yield main_window
    main_window.close()


def test_shows_message_for_invalid_data_failure(window):
    dialog = isni_assignation_failed_message_box(window, NameRegistry.Codes.INVALID_DATA, "Message")
    driver = MessageBoxDriver(WidgetIdentity(dialog), EventProcessingProber(), Robot())
    dialog.open()

    driver.is_showing_message("Could not assign an ISNI")
    driver.is_showing_details("Invalid data: Message")
    driver.acknowledge()


def test_shows_message_for_invalid_format_failure(window):
    dialog = isni_assignation_failed_message_box(window, NameRegistry.Codes.INVALID_FORMAT, "Message")
    driver = MessageBoxDriver(WidgetIdentity(dialog), EventProcessingProber(), Robot())
    dialog.open()

    driver.is_showing_message("Could not assign an ISNI")
    driver.is_showing_details("Invalid format: Message")
    driver.acknowledge()


def test_shows_message_for_sparse_failure(window):
    dialog = isni_assignation_failed_message_box(window, NameRegistry.Codes.SPARSE, "Message")
    driver = MessageBoxDriver(WidgetIdentity(dialog), EventProcessingProber(), Robot())
    dialog.open()

    driver.is_showing_message("Could not assign an ISNI")
    driver.is_showing_details("Sparse data: Message")
    driver.acknowledge()