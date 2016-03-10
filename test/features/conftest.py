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
def platform():
    from test.util import cheddar
    server_thread = cheddar.start()
    yield cheddar
    cheddar.stop(server_thread)
