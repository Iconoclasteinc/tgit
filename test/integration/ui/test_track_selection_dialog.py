# -*- coding: utf-8 -*-
import sys

from hamcrest import contains

from PyQt5.QtWidgets import QMainWindow, QFileDialog
import pytest

from test.cute.prober import EventProcessingProber
from test.cute.robot import Robot
from test.cute.matchers import named
from test.cute.widgets import window
from test.drivers.track_selection_dialog_driver import TrackSelectionDialogDriver
from test.cute.probes import ValueMatcherProbe
from test.integration.ui import show_widget
from test.util import resources
from tgit.ui.track_selection_dialog import TrackSelectionDialog


@pytest.fixture()
def dialog(qt):
    main_window = QMainWindow()
    show_widget(main_window)
    return TrackSelectionDialog(main_window, native=False, transient=False)


@pytest.yield_fixture()
def driver(dialog):
    driver = TrackSelectionDialogDriver(window(QFileDialog, named('track-selection-dialog')),
                                        EventProcessingProber(), Robot())
    yield driver
    driver.close()


def test_signals_when_audio_files_selected(driver, dialog):
    audio_files = [resources.path('audio', 'Rolling in the Deep.mp3'),
                   resources.path('audio', 'Set Fire to the Rain.mp3'),
                   resources.path('audio', 'Someone Like You.mp3')]

    track_selection_signal = ValueMatcherProbe('track(s) selection', audio_files)

    dialog.tracks_selected.connect(track_selection_signal.received)

    dialog.display()
    driver.select_tracks(*audio_files)
    driver.check(track_selection_signal)


def test_alternatively_selects_directories_instead_of_files(driver, dialog):
    audio_folder = resources.path('audio')
    track_selection_signal = ValueMatcherProbe('track(s) selection', contains(audio_folder))
    dialog.tracks_selected.connect(track_selection_signal.received)

    dialog.display(folders=True)
    driver.select_tracks_in_folder(audio_folder)
    driver.check(track_selection_signal)


def test_allows_selection_of_flac_files(driver, dialog):
    flac_files = [resources.path('audio', 'Zumbar.flac')]
    track_selection_signal = ValueMatcherProbe('track(s) selection', flac_files)

    dialog.tracks_selected.connect(track_selection_signal.received)

    dialog.display()
    driver.select_tracks(*flac_files, of_type='flac')
    driver.check(track_selection_signal)


@pytest.mark.skipif(sys.platform.startswith("win"), reason="not supported on Windows")
def test_rejects_non_audio_files(driver, dialog):
    unsupported_file = resources.path('front-cover.jpg')

    dialog.display(folders=False)
    driver.rejects_selection_of(unsupported_file)