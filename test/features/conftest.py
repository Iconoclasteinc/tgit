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

from test.drivers.application_runner import ApplicationRunner
from test.drivers.application_settings_driver import ApplicationSettingsDriver
from test.util import doubles
from test.util.workspace import AlbumWorkspace


@pytest.yield_fixture
def recordings(tmpdir):
    library = doubles.recording_library(tmpdir.mkdir("library"))
    yield library
    library.delete()


@pytest.yield_fixture
def workspace(tmpdir):
    album_workspace = AlbumWorkspace(tmpdir.mkdir("workspace"))
    yield album_workspace
    album_workspace.delete()


@pytest.fixture
def settings_file(tmpdir):
    return tmpdir.join("settings.ini").strpath


@pytest.fixture
def settings(settings_file):
    return ApplicationSettingsDriver(settings_file)


@pytest.yield_fixture
def app(workspace, settings_file):
    runner = ApplicationRunner(workspace, settings_file)
    runner.start()
    yield runner
    runner.stop()


@pytest.yield_fixture()
def name_server():
    from test.util import isni_database
    database_thread = isni_database.start()
    yield isni_database
    isni_database.stop(database_thread)


@pytest.fixture
def platform(name_server, request):
    from test.util import cheddar

    server_thread = cheddar.start(name_server.host(), name_server.port())
    cheddar.token_queue = iter(["token12345"])
    request.addfinalizer(lambda: cheddar.stop(server_thread))
