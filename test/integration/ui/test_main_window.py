# -*- coding: utf-8 -*-

import sys

import pytest

from cute.finders import WidgetIdentity
from cute.probes import ValueMatcherProbe
from test.drivers import MainWindowDriver
from test.integration.ui import show_widget
from test.util import builders as build
from tgit.ui.main_window import MainWindow


def ignore(*args):
    pass


@pytest.yield_fixture()
def main_window(qt):
    window = MainWindow(create_startup_screen=ignore, create_album_screen=ignore)
    show_widget(window)
    yield window
    window.close()


@pytest.yield_fixture()
def driver(main_window, prober, automaton):
    main_window_driver = MainWindowDriver(WidgetIdentity(main_window), prober, automaton)
    yield main_window_driver
    main_window_driver.close()


def test_album_actions_are_initially_disabled(driver):
    driver.has_disabled_album_actions()


def test_actions_are_disabled_once_album_is_closed(main_window, driver):
    main_window.enable_album_actions(build.album())

    main_window.disable_album_actions()
    driver.has_disabled_album_actions()


def test_signals_when_add_files_menu_item_clicked(main_window, driver):
    album = build.album()
    add_files_signal = ValueMatcherProbe("add files", album)
    main_window.add_files.connect(add_files_signal.received)
    main_window.enable_album_actions(album)

    driver.add_tracks_to_album(from_menu=True)
    driver.check(add_files_signal)


def test_signals_when_add_folder_menu_item_clicked(main_window, driver):
    album = build.album()
    add_folder_signal = ValueMatcherProbe("add folder", album)
    main_window.add_folder.connect(add_folder_signal.received)
    main_window.enable_album_actions(album)

    driver.add_tracks_in_folder()
    driver.check(add_folder_signal)


def test_signals_when_export_menu_item_clicked(main_window, driver):
    album = build.album()
    export_album_signal = ValueMatcherProbe("export", album)
    main_window.export.connect(export_album_signal.received)
    main_window.enable_album_actions(album)

    driver.export()
    driver.check(export_album_signal)


def test_signals_when_save_album_menu_item_clicked(main_window, driver):
    album = build.album()
    save_album_signal = ValueMatcherProbe("save", album)
    main_window.save.connect(save_album_signal.received)
    main_window.enable_album_actions(album)

    driver.save()
    driver.check(save_album_signal)


@pytest.mark.skipif(sys.platform.startswith("darwin"), reason="still unstable on Mac")
def test_signals_when_save_album_keyboard_shortcut_is_activated(main_window, driver):
    album = build.album()
    save_album_signal = ValueMatcherProbe("save", album)
    main_window.save.connect(save_album_signal.received)
    main_window.enable_album_actions(album)

    driver.save(using_shortcut=True)
    driver.check(save_album_signal)


def test_signals_when_close_album_menu_item_clicked(main_window, driver):
    album = build.album()
    close_album_signal = ValueMatcherProbe("close", album)
    main_window.close_album.connect(close_album_signal.received)
    main_window.enable_album_actions(album)

    driver.close_album()
    driver.check(close_album_signal)


@pytest.mark.skipif(sys.platform.startswith("darwin"), reason="still unstable on Mac")
def test_signals_when_close_album_keyboard_shortcut_is_activated(main_window, driver):
    album = build.album()
    close_album_signal = ValueMatcherProbe("close", album)
    main_window.close_album.connect(close_album_signal.received)
    main_window.enable_album_actions(album)

    driver.close_album(using_shortcut=True)
    driver.check(close_album_signal)


def test_signals_when_settings_menu_item_clicked(main_window, driver):
    change_settings_signal = ValueMatcherProbe("change settings")
    main_window.settings.connect(change_settings_signal.received)

    driver.settings()
    driver.check(change_settings_signal)
