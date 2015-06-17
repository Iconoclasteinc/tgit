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
import os
from PyQt5.QtWidgets import QFileDialog

import pytest
import sys
from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers.load_album_dialog_driver import LoadAlbumDialogDriver
from test.util import resources
from tgit.ui.load_album_dialog import LoadAlbumDialog


@pytest.fixture()
def dialog(main_window):
    return LoadAlbumDialog(main_window, native=False)


@pytest.yield_fixture()
def driver(dialog, prober, automaton):
    driver = LoadAlbumDialogDriver(window(QFileDialog, named("load_album_dialog")), prober, automaton)
    yield driver
    driver.close()


def test_signals_when_album_selected(dialog, driver):
    album_selected_signal = ValueMatcherProbe("album file selected", resources.path("album_mp3.tgit"))
    dialog.display(lambda dest: album_selected_signal.received(os.path.abspath(dest)))

    driver.load(resources.path("album_mp3.tgit"))
    driver.check(album_selected_signal)


@pytest.mark.skipif(sys.platform.startswith("win"), reason="not supported on Windows")
def test_only_accepts_tgit_album_files(dialog, driver):
    dialog.open()

    driver.rejects_selection_of(resources.path("base.mp3"))
