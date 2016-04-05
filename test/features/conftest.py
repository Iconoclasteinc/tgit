# -*- coding: utf-8 -*-
import pytest

from testing import doubles
from testing.drivers import ApplicationRunner
from testing.workspace import AlbumWorkspace


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
    from testing import cheddar
    server_thread = cheddar.start()
    yield cheddar
    cheddar.stop(server_thread)
