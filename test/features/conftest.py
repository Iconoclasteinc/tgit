# -*- coding: utf-8 -*-
import pytest

from test.util import doubles
from test.util.workspace import AlbumWorkspace
from testing.drivers import ApplicationRunner


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


@pytest.yield_fixture
def app(qt, workspace, settings):
    runner = ApplicationRunner(workspace, settings)
    runner.start()
    yield runner
    runner.stop()


@pytest.yield_fixture()
def platform():
    from test.util import cheddar
    server_thread = cheddar.start()
    yield cheddar
    cheddar.stop(server_thread)
