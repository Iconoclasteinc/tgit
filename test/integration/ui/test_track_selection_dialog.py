# -*- coding: utf-8 -*-
import os
import sys

from hamcrest import contains, contains_inanyorder

from PyQt5.QtWidgets import QFileDialog
import pytest

from cute.matchers import named
from cute.widgets import window
from cute.probes import ValueMatcherProbe
from test.drivers import TrackSelectionDialogDriver
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


def abs_path(selection):
    return list(map(os.path.abspath, selection))


def test_signals_selected_files(driver, dialog):
    mp3s = (resources.path("audio", "Rolling in the Deep.mp3"),
            resources.path("audio", "Set Fire to the Rain.mp3"),
            resources.path("audio", "Someone Like You.mp3"))

    tracks_selection_signal = ValueMatcherProbe("track(s) selection", contains(*mp3s))

    dialog.select_files('mp3', lambda *selection: tracks_selection_signal.received(abs_path(selection)))

    driver.select_tracks(*mp3s)
    driver.check(tracks_selection_signal)


def test_alternatively_selects_files_of_given_type_in_folder(driver, dialog):
    mp3s = (resources.path("audio", "Rolling in the Deep.mp3"),
            resources.path("audio", "Set Fire to the Rain.mp3"),
            resources.path("audio", "Someone Like You.mp3"))

    tracks_selection_signal = ValueMatcherProbe("track(s) selection", contains_inanyorder(*mp3s))

    dialog.select_files_in_folder('mp3', lambda *selection: tracks_selection_signal.received(abs_path(selection)))

    driver.select_tracks_in_folder(resources.path("audio"))
    driver.check(tracks_selection_signal)


def test_restricts_selection_based_on_file_type(driver, dialog):
    flac_file = resources.path("audio", "Zumbar.flac")
    tracks_selection_signal = ValueMatcherProbe("track(s) selection", contains(flac_file))

    dialog.select_files('flac', lambda *selection: tracks_selection_signal.received(abs_path(selection)))

    driver.select_tracks(flac_file)
    driver.check(tracks_selection_signal)


@pytest.mark.skipif(sys.platform.startswith("win"), reason="not supported on Windows")
def test_rejects_non_audio_files(driver, dialog):
    unsupported_file = resources.path('front-cover.jpg')

    dialog.select_files('mp3', on_select=None)

    driver.rejects_selection_of(unsupported_file)
