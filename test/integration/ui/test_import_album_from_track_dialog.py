# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QMainWindow, QFileDialog
import pytest

from cute.prober import EventProcessingProber
from cute.robot import Robot
from cute.matchers import named
from cute.widgets import window
from cute.probes import ValueMatcherProbe
from test.integration.ui import show_widget
from test.util import resources
from test.drivers.import_album_from_track_dialog_driver import ImportAlbumFromTrackDialogDriver
from tgit.ui.import_album_from_track_dialog import ImportAlbumFromTrackDialog


@pytest.yield_fixture()
def import_album_dialog(qt):
    main_window = QMainWindow()
    show_widget(main_window)
    yield ImportAlbumFromTrackDialog(main_window, native=False)
    main_window.close()


@pytest.yield_fixture()
def driver(import_album_dialog):
    dialog_driver = ImportAlbumFromTrackDialogDriver(window(QFileDialog, named('import_album_from_track_dialog')),
                                                     EventProcessingProber(), Robot())
    yield dialog_driver
    dialog_driver.close()


def test_signals_when_track_file_selected(driver, import_album_dialog):
    track_file = resources.path('audio', 'Rolling in the Deep.mp3')
    track_selection_signal = ValueMatcherProbe('track selection', track_file)

    import_album_dialog.track_selected.connect(track_selection_signal.received)
    import_album_dialog.open()

    driver.select_track(track_file)
    driver.check(track_selection_signal)


def test_allows_selection_of_flac_files(driver, import_album_dialog):
    flac_file = resources.path('audio', 'Zumbar.flac')
    track_selection_signal = ValueMatcherProbe('track(s) selection', flac_file)

    import_album_dialog.track_selected.connect(track_selection_signal.received)
    import_album_dialog.open()

    driver.select_track(flac_file, of_type='flac')
    driver.check(track_selection_signal)


@pytest.mark.skipif(sys.platform.startswith("win"), reason="not supported on Windows")
def test_rejects_non_audio_files(driver, import_album_dialog):
    unsupported_file = resources.path('front-cover.jpg')

    import_album_dialog.open()

    driver.rejects_selection_of(unsupported_file)