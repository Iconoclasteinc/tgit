# -*- coding: utf-8 -*-
import os
import sys

from hamcrest import assert_that, equal_to, contains
import pytest

from cute.finders import WidgetIdentity
from cute.probes import ValueMatcherProbe
from test.drivers import MainWindowDriver
from test.integration.ui import show_widget
from test.util import builders as build, resources
from test.util.doubles import album_screen, FakeAlbumScreen
from tgit.ui import message_box as message, Dialogs
from tgit.ui.main_window import MainWindow


def ignore(*_):
    pass


@pytest.fixture()
def fake_album_screen():
    return album_screen()


@pytest.yield_fixture()
def main_window(qt, fake_album_screen):
    def create_fake_album_screen(album):
        return fake_album_screen

    dialogs = Dialogs(commands=None, native=False)
    window = MainWindow(portfolio=build.album_portfolio(),
                        create_startup_screen=ignore,
                        create_album_screen=create_fake_album_screen,
                        create_close_album_confirmation=message.close_album_confirmation_box,
                        select_export_destination=dialogs.export,
                        select_tracks=dialogs.add_tracks,
                        confirm_exit=False)
    dialogs.parent = window
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
    filename = resources.path("audio", "Zumbar.flac")
    add_files_signal = ValueMatcherProbe("add files", contains(album, filename))
    main_window.on_add_files(lambda current_album, file: add_files_signal.received([album, os.path.abspath(file)]))
    main_window.display_album_screen(album)

    driver.add_tracks_to_album(filename, from_menu=True)
    driver.check(add_files_signal)


def test_signals_when_add_folder_menu_item_clicked(main_window, driver):
    album = build.album()
    add_folder_signal = ValueMatcherProbe("add folder", album)
    main_window.add_folder.connect(add_folder_signal.received)
    main_window.enable_album_actions(album)

    driver.add_tracks_in_folder()
    driver.check(add_folder_signal)


def test_signals_when_export_menu_item_clicked(main_window, driver, tmpdir):
    album = build.album()
    export_signal = ValueMatcherProbe("export", contains(album, tmpdir.join("album.csv").strpath))
    main_window.on_export(
        lambda current_album, destination: export_signal.received((current_album, os.path.abspath(destination))))
    main_window.display_album_screen(album)
    driver.export(tmpdir.join("album.csv").strpath)
    driver.check(export_signal)


def test_signals_when_save_album_menu_item_clicked(main_window, driver):
    album = build.album()
    save_album_signal = ValueMatcherProbe("save", album)
    main_window.on_save_album(save_album_signal.received)
    main_window.display_album_screen(album)

    driver.save()
    driver.check(save_album_signal)


@pytest.mark.skipif(sys.platform.startswith("darwin"), reason="still unstable on Mac")
def test_signals_when_save_album_keyboard_shortcut_is_activated(main_window, driver):
    album = build.album()
    save_album_signal = ValueMatcherProbe("save", album)
    main_window.on_save_album(save_album_signal.received)
    main_window.display_album_screen(album)

    driver.save(using_shortcut=True)
    driver.check(save_album_signal)


def test_shows_confirmation_when_close_album_menu_item_clicked(main_window, driver):
    main_window.enable_album_actions(build.album())
    driver.close_album()


@pytest.mark.skipif(sys.platform.startswith("darwin"), reason="still unstable on Mac")
def test_shows_confirmation_when_close_album_keyboard_shortcut_is_activated(main_window, driver):
    main_window.enable_album_actions(build.album())
    driver.close_album(using_shortcut=True)


def test_signals_when_settings_menu_item_clicked(main_window, driver):
    change_settings_signal = ValueMatcherProbe("change settings")
    main_window.on_settings(lambda checked: change_settings_signal.received())

    driver.settings()
    driver.check(change_settings_signal)


def test_navigates_to_album_edition_page_item_when_menu_item_is_clicked(main_window, driver, fake_album_screen):
    album = build.album()
    main_window.display_album_screen(album)

    driver.navigate_to_album_page()
    assert_that(fake_album_screen.current_page, equal_to(FakeAlbumScreen.ALBUM_EDITION_PAGE))


def test_navigates_to_album_composition_page_item_when_menu_item_is_clicked(main_window, driver, fake_album_screen):
    album = build.album()
    main_window.display_album_screen(album)

    driver.navigate_to_album_page()
    driver.navigate_to_composition_page()
    assert_that(fake_album_screen.current_page, equal_to(FakeAlbumScreen.ALBUM_COMPOSITION_PAGE))


def test_adds_track_menu_item_when_adding_a_track_to_the_album(main_window, driver):
    album = build.album()
    main_window.display_album_screen(album)
    album.add_track(build.track(track_title="Chevere!"))

    driver.shows_track_menu_item(title="Chevere!", track_number=1)


def test_removes_track_menu_item_when_removing_a_track_from_the_album(main_window, driver):
    album = build.album()
    main_window.display_album_screen(album)

    track = build.track(track_title="Chevere!")
    album.add_track(track)
    album.remove_track(track)

    driver.does_not_show_menu_item(title="Chevere!", track_number=1)


def test_displays_track_menu_item_when_loading_an_existing_album(main_window, driver):
    album = build.album(tracks=[build.track(track_title="Chevere!"), build.track(track_title="Zumbar")])
    main_window.display_album_screen(album)

    driver.shows_track_menu_item(title="Chevere!", track_number=1)
    driver.shows_track_menu_item(title="Zumbar", track_number=2)


def test_removes_track_menu_item_when_closing_an_album(main_window, driver):
    album = build.album(tracks=[build.track(track_title="Chevere!"), build.track(track_title="Zumbar")])
    main_window.display_album_screen(album)

    main_window.display_startup_screen()

    album = build.album()
    main_window.display_album_screen(album)

    driver.does_not_show_menu_item(title="Chevere!", track_number=1)
    driver.does_not_show_menu_item(title="Zumbar", track_number=2)


def test_navigates_to_track_page_when_menu_item_is_clicked(main_window, driver, fake_album_screen):
    album = build.album()
    main_window.display_album_screen(album)
    album.add_track(build.track(track_title="Chevere!"))
    album.add_track(build.track(track_title="Zumbar"))
    album.add_track(build.track(track_title="Salsa Coltrane"))

    driver.navigate_to_track_page(title="Salsa Coltrane", track_number=3)
    assert_that(fake_album_screen.current_page, equal_to(FakeAlbumScreen.TRACK_3))
