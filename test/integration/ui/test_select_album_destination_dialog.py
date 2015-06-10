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

from hamcrest import equal_to
from PyQt5.QtWidgets import QFileDialog
import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers.select_album_destination_dialog_driver import SelectAlbumDestinationDialogDriver
from tgit.ui.select_album_destination_dialog import SelectAlbumDestinationDialog


@pytest.fixture()
def dialog(main_window):
    return SelectAlbumDestinationDialog(main_window, native=False)


@pytest.yield_fixture()
def driver(dialog, prober, automaton):
    dialog_driver = SelectAlbumDestinationDialogDriver(window(QFileDialog, named("select_album_destination_dialog")),
                                                       prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def test_signals_save_as_destination(tmpdir, dialog, driver):
    destination = tmpdir.join("album.tgit").strpath
    save_as_signal = ValueMatcherProbe("select destination", equal_to(destination))

    dialog.display(lambda dest: save_as_signal.received(os.path.abspath(dest)))

    driver.save_as("album.tgit", tmpdir.strpath)
    driver.check(save_as_signal)


def test_automatically_appends_extention(tmpdir, dialog, driver):
    destination = tmpdir.join("album.tgit").strpath
    save_as_signal = ValueMatcherProbe("select destination", equal_to(destination))

    dialog.display(lambda dest: save_as_signal.received(os.path.abspath(dest)))

    driver.save_as("album", tmpdir.strpath)
    driver.check(save_as_signal)
