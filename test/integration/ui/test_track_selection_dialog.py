# -*- coding: utf-8 -*-
import sys

from hamcrest import contains
from PyQt5.QtWidgets import QMainWindow, QFileDialog
import pytest

from cute.prober import EventProcessingProber
from cute.robot import Robot
from cute.matchers import named
from cute.widgets import window
from cute.probes import ValueMatcherProbe
from test.drivers import TrackSelectionDialogDriver
from test.integration.ui import show_widget
from test.util import resources
from tgit.album import Album
from tgit.ui.track_selection_dialog import TrackSelectionDialog


@pytest.yield_fixture()
def dialog(qt):
    main_window = QMainWindow()
    show_widget(main_window)
    yield TrackSelectionDialog(main_window, native=False)
    main_window.close()


@pytest.yield_fixture()
def driver(dialog):
    dialog_driver = TrackSelectionDialogDriver(window(QFileDialog, named('track-selection-dialog')),
                                               EventProcessingProber(), Robot())
    yield dialog_driver
    dialog_driver.close()


def test_signals_when_audio_files_selected(driver, dialog):
    audio_files = [resources.path("audio", "Rolling in the Deep.mp3"),
                   resources.path("audio", "Set Fire to the Rain.mp3"),
                   resources.path("audio", "Someone Like You.mp3")]

    track_selection_signal = ValueMatcherProbe("track(s) selection", audio_files)

    dialog.tracks_selected.connect(track_selection_signal.received)

    dialog.display(Album(of_type=Album.Type.MP3))
    driver.select_tracks(*audio_files)
    driver.check(track_selection_signal)


def test_alternatively_selects_directories_instead_of_files(driver, dialog):
    audio_folder = resources.path("audio")
    track_selection_signal = ValueMatcherProbe("track(s) selection", contains(audio_folder))
    dialog.tracks_selected.connect(track_selection_signal.received)

    dialog.display(Album(), folders=True)
    driver.select_tracks_in_folder(audio_folder)
    driver.check(track_selection_signal)


def test_allows_selection_of_flac_files(driver, dialog):
    flac_files = [resources.path("audio", "Zumbar.flac")]
    track_selection_signal = ValueMatcherProbe("track(s) selection", flac_files)

    dialog.tracks_selected.connect(track_selection_signal.received)

    dialog.display(Album(of_type=Album.Type.FLAC))
    driver.select_tracks(*flac_files)
    driver.check(track_selection_signal)


@pytest.mark.skipif(sys.platform.startswith("win"), reason="not supported on Windows")
def test_rejects_non_audio_files(driver, dialog):
    unsupported_file = resources.path('front-cover.jpg')

    dialog.display(folders=False)
    driver.rejects_selection_of(unsupported_file)