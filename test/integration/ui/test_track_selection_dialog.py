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
from tgit.ui.track_selection_dialog import TrackSelectionDialog


@pytest.fixture()
def dialog(main_window):
    return TrackSelectionDialog(main_window, native=False)


@pytest.yield_fixture()
def driver(dialog, prober, automaton):
    dialog_driver = TrackSelectionDialogDriver(window(QFileDialog, named('track-selection-dialog')), prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def test_signals_when_audio_files_selected(driver, dialog):
    audio_files = [resources.path("audio", "Rolling in the Deep.mp3"),
                   resources.path("audio", "Set Fire to the Rain.mp3"),
                   resources.path("audio", "Someone Like You.mp3")]

    track_selection_signal = ValueMatcherProbe("track(s) selection", audio_files)

    dialog.tracks_selected.connect(track_selection_signal.received)
    dialog.open()

    driver.select_tracks(*audio_files)
    driver.check(track_selection_signal)


def test_alternatively_selects_directories_instead_of_files(driver, dialog):
    audio_folder = resources.path("audio")
    track_selection_signal = ValueMatcherProbe("track(s) selection", contains(audio_folder))

    dialog.tracks_selected.connect(track_selection_signal.received)
    dialog.select_folders()
    dialog.open()

    driver.select_tracks_in_folder(audio_folder)
    driver.check(track_selection_signal)


def test_allows_selection_of_flac_files(driver, dialog):
    flac_files = [resources.path("audio", "Zumbar.flac")]
    track_selection_signal = ValueMatcherProbe("track(s) selection", flac_files)

    dialog.tracks_selected.connect(track_selection_signal.received)
    dialog.filter_tracks('flac')
    dialog.open()

    driver.select_tracks(*flac_files)
    driver.check(track_selection_signal)


@pytest.mark.skipif(sys.platform.startswith("win"), reason="not supported on Windows")
def test_rejects_non_audio_files(driver, dialog):
    unsupported_file = resources.path('front-cover.jpg')

    dialog.open()

    driver.rejects_selection_of(unsupported_file)