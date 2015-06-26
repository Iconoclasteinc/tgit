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
import sys

from PyQt5.QtWidgets import QFileDialog
from hamcrest import ends_with
import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers.load_album_dialog_driver import LoadAlbumDialogDriver
from test.util import resources
from tgit.ui.load_album_dialog import LoadAlbumDialog

do_nothing = lambda *_: None


DISPLAY_DELAY = 250


@pytest.fixture()
def dialog(qt):
    return LoadAlbumDialog(native=False)


@pytest.yield_fixture()
def driver(dialog, prober, automaton):
    dialog_driver = LoadAlbumDialogDriver(window(QFileDialog, named("load_album_dialog")), prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def ignore(*args):
    pass


def test_signals_when_album_selected(dialog, driver):
    album_selected_signal = ValueMatcherProbe("album file selected", resources.path("album.tgit"))
    dialog.select(lambda dest: album_selected_signal.received(os.path.abspath(dest)))

    driver.load(resources.path("album.tgit"))
    driver.check(album_selected_signal)


@pytest.mark.skipif(sys.platform.startswith("win"), reason="not supported on Windows")
def test_only_accepts_tgit_album_files(dialog, driver):
    dialog.select(ignore)

    driver.rejects_selection_of(resources.path("base.mp3"))


def test_initially_starts_in_documents_folder(driver):
    driver.has_current_directory(ends_with("Documents"))
