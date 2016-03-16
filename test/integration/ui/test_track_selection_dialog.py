import os

import pytest
from PyQt5.QtWidgets import QFileDialog
from hamcrest import contains, contains_inanyorder, ends_with

from cute.matchers import named
from cute.platforms import linux
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers import TrackSelectionDialogDriver
from test.integration.ui import ignore
from test.util import resources
from tgit.platforms import windows
from tgit.ui.dialogs.track_selection_dialog import TrackSelectionDialog

pytestmark = pytest.mark.ui


def show_dialog(of_type="mp3", on_select_file=ignore, on_select_files=ignore, on_select_files_in_folder=ignore):
    dialog = TrackSelectionDialog(native=False)
    if on_select_file != ignore:
        dialog.select_file(of_type, on_select_file)

    if on_select_files != ignore:
        dialog.select_files(of_type, on_select_files)

    if on_select_files_in_folder != ignore:
        dialog.select_files_in_folder(of_type, on_select_files_in_folder)

    return dialog


@pytest.fixture()
def driver(qt, prober, automaton):
    return TrackSelectionDialogDriver(window(QFileDialog, named('track-selection-dialog')), prober, automaton)


def _abs_path(selection):
    return list(map(os.path.abspath, selection))


def test_signals_selected_file(driver):
    mp3 = resources.path("audio", "Rolling in the Deep.mp3")
    track_selection_signal = ValueMatcherProbe("track selection", mp3)

    _ = show_dialog(on_select_file=lambda sel: track_selection_signal.received(os.path.abspath(sel)))

    driver.select_tracks(mp3)
    driver.check(track_selection_signal)


def test_signals_selected_files(driver):
    mp3s = (resources.path("audio", "Rolling in the Deep.mp3"),
            resources.path("audio", "Set Fire to the Rain.mp3"),
            resources.path("audio", "Someone Like You.mp3"))

    tracks_selection_signal = ValueMatcherProbe("track(s) selection", contains(*mp3s))

    _ = show_dialog(on_select_files=lambda *sel: tracks_selection_signal.received(_abs_path(sel)))

    driver.select_tracks(*mp3s)
    driver.check(tracks_selection_signal)


def test_alternatively_selects_files_of_given_type_in_folder(driver):
    mp3s = (resources.path("audio", "Rolling in the Deep.mp3"),
            resources.path("audio", "Set Fire to the Rain.mp3"),
            resources.path("audio", "Someone Like You.mp3"))

    tracks_selection_signal = ValueMatcherProbe("track(s) selection", contains_inanyorder(*mp3s))

    _ = show_dialog(on_select_files_in_folder=lambda *sel: tracks_selection_signal.received(_abs_path(sel)))

    driver.select_tracks_in_folder(resources.path("audio"))
    driver.check(tracks_selection_signal)


def test_restricts_selection_based_on_file_type(driver):
    flac_file = resources.path("audio", "Zumbar.flac")
    tracks_selection_signal = ValueMatcherProbe("track(s) selection", contains(flac_file))

    _ = show_dialog("flac", on_select_files=lambda *sel: tracks_selection_signal.received(_abs_path(sel)))

    driver.select_tracks(flac_file)
    driver.check(tracks_selection_signal)


@pytest.mark.skipif(windows, reason="not supported on Windows")
@pytest.mark.skipif(linux, reason="not supported on Linux")
def test_only_accept_audio_files(driver):
    unsupported_file = resources.path("front-cover.jpg")

    _ = show_dialog(on_select_file=lambda: None)

    driver.rejects_selection_of(unsupported_file)


def test_initially_starts_in_user_music_folder(driver):
    _ = show_dialog()
    driver.has_current_directory(ends_with("Music"))
