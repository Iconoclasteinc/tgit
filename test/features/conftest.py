# -*- coding: utf-8 -*-
import pytest

from test.drivers.application_runner import ApplicationRunner
from test.util import doubles
from test.util.workspace import AlbumWorkspace
from tgit.settings_backend import SettingsBackend


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


@pytest.yield_fixture
def app(qt, workspace, settings_file):
    runner = ApplicationRunner(workspace, SettingsBackend(settings_file))
    runner.start()
    yield runner
    runner.stop()


@pytest.yield_fixture()
def platform():
    from test.util import cheddar
    server_thread = cheddar.start()
    yield cheddar
    cheddar.stop(server_thread)
