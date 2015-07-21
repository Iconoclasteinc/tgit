# -*- coding: utf-8 -*-
import sys

from hamcrest import contains, instance_of
import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers import MainWindowDriver
from test.drivers.fake_drivers import no_startup_screen, no_album_screen, album_screen, startup_screen
from test.integration.ui import show_widget
from test.integration.ui.fake_widgets import fake_startup_screen, fake_album_screen
from test.util import builders as build
from test.util.builders import make_album
from tgit.album import Album
from tgit.ui.main_window import MainWindow

ignore = lambda *_, **__: None
yes = lambda: True


def raise_os_error(message):
    def raise_error(*_):
        raise OSError(message)

    return raise_error


def show_page(portfolio=build.album_portfolio(),
              create_startup_screen=fake_startup_screen,
              create_album_screen=fake_album_screen,
              confirm_close=ignore,
              show_save_error=ignore,
              show_export_error=ignore,
              select_export_destination=ignore,
              select_tracks=ignore,
              select_tracks_in_folder=ignore,
              confirm_exit=yes,
              **handlers):
    main_window = MainWindow(portfolio=portfolio,
                             confirm_exit=confirm_exit,
                             create_startup_screen=create_startup_screen,
                             create_album_screen=create_album_screen,
                             confirm_close=confirm_close,
                             show_save_error=show_save_error,
                             show_export_error=show_export_error,
                             select_export_destination=select_export_destination,
                             select_tracks=select_tracks,
                             select_tracks_in_folder=select_tracks_in_folder,
                             **handlers)
    show_widget(main_window)

    return main_window


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    main_window_driver = MainWindowDriver(window(MainWindow, named("main_window")), prober, automaton)
    yield main_window_driver
    main_window_driver.close()


def test_album_actions_are_initially_disabled(driver):
    show_page()
    driver.has_disabled_album_actions()


def test_actions_are_disabled_once_album_is_closed(driver):
    main_window = show_page()
    main_window.enable_album_actions(build.album())

    main_window.disable_album_actions()
    driver.has_disabled_album_actions()


def test_signals_when_add_files_menu_item_clicked(driver):
    main_window = show_page(
        select_tracks=lambda type_, on_select: on_select("track1." + type_, "track2." + type_))
    album = build.album(of_type=Album.Type.FLAC)
    add_files_signal = ValueMatcherProbe("add files", contains(album, ("track1.flac", "track2.flac")))
    main_window.on_add_files(lambda current_album, *files: add_files_signal.received([album, files]))
    main_window.display_album_screen(album)

    driver.add_tracks_to_album(from_menu=True)
    driver.check(add_files_signal)


def test_signals_when_add_folder_menu_item_clicked(driver):
    main_window = show_page(
        select_tracks_in_folder=lambda type_, on_select: on_select("track1." + type_, "track2." + type_))
    album = build.album()
    add_folder_signal = ValueMatcherProbe("add folder", contains(album, ("track1.flac", "track2.flac")))
    main_window.on_add_files(lambda current_album, *file: add_folder_signal.received([current_album, file]))
    main_window.display_album_screen(album)

    driver.add_tracks_in_folder()
    driver.check(add_folder_signal)


def test_signals_when_export_menu_item_clicked(driver):
    main_window = show_page(select_export_destination=lambda on_select, name: on_select(name + ".csv"))
    album = build.album(release_name="Honeycomb")
    export_signal = ValueMatcherProbe("export", contains(album, "Honeycomb.csv"))
    main_window.on_export(
        lambda current_album, destination: export_signal.received([current_album, destination]))
    main_window.display_album_screen(album)

    driver.export()
    driver.check(export_signal)


def test_signals_when_save_album_menu_item_clicked(driver):
    album = make_album()
    save_album_signal = ValueMatcherProbe("save", album)

    main_window = show_page(on_save_album=save_album_signal.received)
    main_window.display_album_screen(album)

    driver.save()
    driver.check(save_album_signal)


def test_signals_when_about_qt_menu_item_clicked(driver):
    about_qt_signal = ValueMatcherProbe("about Qt")

    show_page(on_about_qt=lambda pressed: about_qt_signal.received())

    driver.about_qt()
    driver.check(about_qt_signal)


def test_signals_when_about_menu_item_clicked(driver):
    about_signal = ValueMatcherProbe("about")

    show_page(on_about=lambda pressed: about_signal.received())

    driver.about()
    driver.check(about_signal)


@pytest.mark.skipif(sys.platform.startswith("darwin"), reason="still unstable on Mac")
def test_signals_when_save_album_keyboard_shortcut_is_activated(driver):
    album = make_album()
    save_album_signal = ValueMatcherProbe("save", album)

    main_window = show_page(on_save_album=save_album_signal.received)
    main_window.display_album_screen(album)

    driver.save(using_shortcut=True)
    driver.check(save_album_signal)


def test_asks_for_confirmation_before_closing_album(driver):
    album = make_album()
    confirm_close_query = ValueMatcherProbe("confirm close")

    main_window = show_page(confirm_close=lambda **_: confirm_close_query.received(), on_close_album=ignore)
    main_window.display_album_screen(album)

    driver.close_album()
    driver.check(confirm_close_query)


def test_signals_when_album_closed(driver):
    album = make_album()
    close_album_signal = ValueMatcherProbe("close", album)

    main_window = show_page(confirm_close=lambda on_accept: on_accept(), on_close_album=close_album_signal.received)
    main_window.display_album_screen(album)

    driver.close_album()
    driver.check(close_album_signal)


@pytest.mark.skipif(sys.platform.startswith("darwin"), reason="still unstable on Mac")
def test_shows_confirmation_when_close_album_keyboard_shortcut_is_activated(driver):
    main_window = show_page()
    main_window.enable_album_actions(build.album())
    driver.close_album(using_shortcut=True)


def test_signals_when_settings_menu_item_clicked(driver):
    main_window = show_page()
    change_settings_signal = ValueMatcherProbe("change settings")
    main_window.on_settings(lambda checked: change_settings_signal.received())

    driver.settings()
    driver.check(change_settings_signal)


def test_navigates_to_album_edition_page_item_when_menu_item_is_clicked(driver):
    main_window = show_page()
    album = build.album()
    main_window.display_album_screen(album)

    driver.navigate_to_album_page()
    album_screen(driver).is_showing_album_edition_page()


def test_navigates_to_track_list_page_item_when_menu_item_is_clicked(driver):
    main_window = show_page()
    album = build.album()
    main_window.display_album_screen(album)

    driver.navigate_to_album_page()
    driver.navigate_to_track_list_page()
    album_screen(driver).is_showing_track_list_page()


def test_adds_track_menu_item_when_adding_a_track_to_the_album(driver):
    main_window = show_page()
    album = build.album()
    main_window.display_album_screen(album)
    album.add_track(build.track(track_title="Chevere!"))

    driver.shows_track_menu_item(title="Chevere!", track_number=1)


def test_updates_track_menu_item_when_track_name_changes(driver):
    main_window = show_page()
    album = build.album()
    main_window.display_album_screen(album)
    album.add_track(build.track(track_title="Chevere!"))
    album.tracks[0].track_title = "Zumbar"

    driver.shows_track_menu_item(title="Zumbar", track_number=1)


def test_removes_track_menu_item_when_removing_a_track_from_the_album(driver):
    main_window = show_page()
    album = build.album()
    main_window.display_album_screen(album)

    track = build.track(track_title="Chevere!")
    album.add_track(track)
    album.remove_track(track)

    driver.does_not_show_menu_item(title="Chevere!", track_number=1)


def test_displays_track_menu_item_when_loading_an_existing_album(driver):
    main_window = show_page()
    album = build.album(tracks=[build.track(track_title="Chevere!"), build.track(track_title="Zumbar")])
    main_window.display_album_screen(album)

    driver.shows_track_menu_item(title="Chevere!", track_number=1)
    driver.shows_track_menu_item(title="Zumbar", track_number=2)


def test_removes_track_menu_item_when_closing_an_album(driver):
    main_window = show_page()
    album = build.album(tracks=[build.track(track_title="Chevere!"), build.track(track_title="Zumbar")])
    main_window.display_album_screen(album)

    main_window.display_startup_screen()

    album = build.album()
    main_window.display_album_screen(album)

    driver.does_not_show_menu_item(title="Chevere!", track_number=1)
    driver.does_not_show_menu_item(title="Zumbar", track_number=2)


def test_navigates_to_track_page_when_menu_item_is_clicked(driver):
    main_window = show_page()
    album = build.album()
    main_window.display_album_screen(album)
    album.add_track(build.track(track_title="Chevere!"))
    album.add_track(build.track(track_title="Zumbar"))
    album.add_track(build.track(track_title="Salsa Coltrane"))

    driver.navigate_to_track_page(title="Salsa Coltrane", track_number=3)
    album_screen(driver).is_showing_track_edition_page(3)


def test_closes_main_widget_when_changing_page(driver):
    main_window = show_page()
    album = build.album()

    screen = startup_screen(driver).widget()
    main_window.display_album_screen(album)
    no_startup_screen(driver).exists()
    screen.is_closed()

    screen = album_screen(driver).widget()
    main_window.display_startup_screen()
    no_album_screen(driver).exists()
    screen.is_closed()


def test_warn_user_if_save_failed(driver):
    save_failed_signal = ValueMatcherProbe("save album failed", instance_of(OSError))
    album = make_album()

    page = show_page(on_save_album=raise_os_error("Save failed"), show_save_error=save_failed_signal.received)
    page.display_album_screen(album)

    driver.save()
    driver.check(save_failed_signal)


def test_warn_user_if_export_failed(driver):
    def on_export(callback, _):
        callback("...")

    export_failed_signal = ValueMatcherProbe("export failed", instance_of(OSError))
    album = make_album()

    page = show_page(on_export=raise_os_error("Export failed"), show_export_error=export_failed_signal.received,
                     select_export_destination=on_export)
    page.display_album_screen(album)

    driver.export()
    driver.check(export_failed_signal)
