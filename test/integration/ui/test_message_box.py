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

from cute.finders import WidgetIdentity
from cute.probes import ValueMatcherProbe
from cute.widgets import QMessageBoxDriver
from tgit.ui import isni_assignation_failed_message_box
from tgit.ui.message_box import close_album_confirmation_box


def test_shows_isni_assignation_failed_message_with_details(qt, prober, automaton):
    dialog = isni_assignation_failed_message_box(details="Details")
    driver = QMessageBoxDriver(WidgetIdentity(dialog), prober, automaton)
    dialog.open()

    driver.is_active()
    driver.shows_message("Could not assign an ISNI")
    driver.shows_details("Details")
    driver.ok()


def test_shows_close_album_message(qt, prober, automaton):
    dialog = close_album_confirmation_box()
    driver = QMessageBoxDriver(WidgetIdentity(dialog), prober, automaton)
    dialog.open()

    driver.is_active()
    driver.shows_message("Are you sure you want to stop working on this release?")
    driver.close()


def test_signals_confirmation_of_closing(qt, prober, automaton):
    accept_signal = ValueMatcherProbe("accept confirmation")
    dialog = close_album_confirmation_box(on_accept=accept_signal.received)
    driver = QMessageBoxDriver(WidgetIdentity(dialog), prober, automaton)
    dialog.open()

    driver.is_active()
    driver.yes()
    driver.check(accept_signal)
