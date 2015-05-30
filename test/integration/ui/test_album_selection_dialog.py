# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QFileDialog
import pytest

from cute.matchers import named
from cute.widgets import window
from cute.probes import ValueMatcherProbe
from test.util import resources
from test.drivers import ImportAlbumFromTrackDialogDriver
from tgit.ui.album_selection_dialog import AlbumSelectionDialog


@pytest.fixture()
def dialog(main_window):
    return AlbumSelectionDialog(main_window, native=False)


@pytest.yield_fixture()
def driver(dialog, prober, automaton):
    dialog_driver = ImportAlbumFromTrackDialogDriver(window(QFileDialog, named('import_album_from_track_dialog')),
                                                     prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def test_signals_when_file_selected(driver, dialog):
    track_file = resources.path('audio', 'Rolling in the Deep.mp3')
    track_selection_signal = ValueMatcherProbe('track selection', track_file)

    dialog.track_selected.connect(track_selection_signal.received)
    dialog.open()

    driver.select_track(track_file)
    driver.check(track_selection_signal)


def test_allows_selection_of_flac_files(driver, dialog):
    flac_file = resources.path('audio', 'Zumbar.flac')
    track_selection_signal = ValueMatcherProbe('track(s) selection', flac_file)

    dialog.track_selected.connect(track_selection_signal.received)
    dialog.open()

    driver.select_track(flac_file, of_type='flac')
    driver.check(track_selection_signal)


@pytest.mark.skipif(sys.platform.startswith("win"), reason="not supported on Windows")
def test_rejects_non_audio_files(driver, dialog):
    unsupported_file = resources.path('front-cover.jpg')

    dialog.open()

    driver.rejects_selection_of(unsupported_file)