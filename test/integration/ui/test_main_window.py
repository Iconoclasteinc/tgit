# -*- coding: utf-8 -*-

import sys
from hamcrest import assert_that, equal_to

import pytest

from cute.finders import WidgetIdentity
from cute.probes import ValueMatcherProbe
from test.drivers import MainWindowDriver, message_box, export_as_dialog
from test.integration.ui import show_widget
from test.util import builders as build
from test.util.doubles import album_screen, FakeAlbumScreen
from tgit.ui import message_box as message, Dialogs
from tgit.ui.main_window import MainWindow


def ignore(*args):
    pass


@pytest.fixture()
def fake_album_screen():
    return album_screen()


@pytest.fixture()
def create_album_screen(fake_album_screen):
    def create_fake_album_screen(album):
        return fake_album_screen

    return create_fake_album_screen


@pytest.yield_fixture()
def main_window(qt, create_album_screen):
    dialogs = Dialogs(commands=None, native=False)
    window = MainWindow(create_startup_screen=ignore, create_album_screen=create_album_screen,
                        create_close_album_confirmation=message.close_album_confirmation_box,
                        select_export_destination=dialogs.export)
    dialogs.parent=window
    show_widget(window)
    yield window
    window.close()


@pytest.yield_fixture()
def driver(main_window, prober, automaton):
    main_window_driver = MainWindowDriver(WidgetIdentity(main_window), prober, automaton)
    yield main_window_driver
    main_window_driver.close()


@pytest.yield_fixture()
def export_as_dialog_driver(driver):
    export_as_driver = export_as_dialog(driver)
    yield export_as_driver
    export_as_driver.close()


@pytest.yield_fixture()
def message_box_driver(driver):
    message_driver = message_box(driver)
    yield message_driver
    message_driver.close()


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


def test_signals_when_export_menu_item_clicked(main_window, driver, export_as_dialog_driver):
    album = build.album()
    main_window.enable_album_actions(album)
    driver.export()
    export_as_dialog_driver.is_showing_on_screen()
    export_as_dialog_driver.reject()


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


def test_shows_confirmation_when_close_album_menu_item_clicked(main_window, driver, message_box_driver):
    main_window.enable_album_actions(build.album())
    driver.close_album()
    message_box_driver.is_showing_on_screen()
    message_box_driver.yes()


@pytest.mark.skipif(sys.platform.startswith("darwin"), reason="still unstable on Mac")
def test_shows_confirmation_when_close_album_keyboard_shortcut_is_activated(main_window, driver, message_box_driver):
    main_window.enable_album_actions(build.album())
    driver.close_album()
    message_box_driver.is_showing_on_screen()
    message_box_driver.yes()


def test_signals_when_settings_menu_item_clicked(main_window, driver):
    change_settings_signal = ValueMatcherProbe("change settings")
    main_window.settings.connect(change_settings_signal.received)

    driver.settings()
    driver.check(change_settings_signal)


def test_navigates_to_album_edition_page_item_is_clicked(main_window, driver, fake_album_screen):
    album = build.album()
    main_window.display_album_screen(album)

    driver.navigate_to_album_page()
    assert_that(fake_album_screen.current_page, equal_to(FakeAlbumScreen.ALBUM_EDITION_PAGE))
