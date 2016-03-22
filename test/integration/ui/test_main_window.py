# -*- coding: utf-8 -*-
import pytest
from hamcrest import contains, instance_of

from cute.matchers import named
from cute.probes import ValueMatcherProbe, MultiValueMatcherProbe
from cute.widgets import window
from test.drivers import MainWindowDriver
from test.drivers.fake_drivers import no_startup_screen, no_album_screen, project_screen, startup_screen
from test.integration.ui import ignore, show_
from test.integration.ui.fake_widgets import fake_startup_screen, fake_project_screen
from test.util import builders as build
from test.util.builders import make_album, make_portfolio, make_anonymous_session
from tgit.album import Album
from tgit.auth import User
from tgit.platforms import mac
from tgit.ui.main_window import MainWindow

pytestmark = pytest.mark.ui


def yes():
    return True


def _raise_os_error(message):
    def raise_error(*_):
        raise OSError(message)

    return raise_error


def show_main_window(session=make_anonymous_session(),
                     portfolio=make_portfolio(),
                     create_startup_screen=fake_startup_screen,
                     create_project_screen=fake_project_screen,
                     confirm_close=ignore,
                     show_save_error=ignore,
                     show_export_error=ignore,
                     select_export_destination=ignore,
                     select_save_as_destination=ignore,
                     select_tracks=ignore,
                     select_tracks_in_folder=ignore,
                     confirm_exit=yes,
                     **handlers):
    main_window = MainWindow(session=session,
                             portfolio=portfolio,
                             confirm_exit=confirm_exit,
                             create_startup_screen=create_startup_screen,
                             create_project_screen=create_project_screen,
                             confirm_close=confirm_close,
                             show_save_error=show_save_error,
                             show_export_error=show_export_error,
                             select_export_destination=select_export_destination,
                             select_save_as_destination=select_save_as_destination,
                             select_tracks=select_tracks,
                             select_tracks_in_folder=select_tracks_in_folder,
                             **handlers)
    show_(main_window)

    return main_window


@pytest.yield_fixture()
def driver(prober, automaton):
    main_window_driver = MainWindowDriver(window(MainWindow, named("main_window")), prober, automaton)
    yield main_window_driver
    main_window_driver.close()


def test_project_actions_are_initially_disabled(driver):
    _ = show_main_window()
    driver.has_disabled_project_actions()


def test_actions_are_disabled_once_project_is_closed(driver):
    window = show_main_window()
    window.enable_project_actions(build.album())

    window.disable_project_actions()
    driver.has_disabled_project_actions()


def test_signals_when_add_files_menu_item_clicked(driver):
    window = show_main_window(select_tracks=lambda type_, on_select: on_select("track1." + type_, "track2." + type_))
    album = build.album(of_type=Album.Type.FLAC)
    add_files_signal = ValueMatcherProbe("add files", contains(album, ("track1.flac", "track2.flac")))
    window.on_add_files(lambda current_album, *files: add_files_signal.received([album, files]))
    window.display_album_screen(album)

    driver.add_tracks_to_project(from_menu=True)
    driver.check(add_files_signal)


def test_signals_when_add_folder_menu_item_clicked(driver):
    window = show_main_window(select_tracks_in_folder=lambda type_, on_select: on_select("track1." + type_,
                                                                                         "track2." + type_))
    album = build.album()
    add_folder_signal = ValueMatcherProbe("add folder", contains(album, ("track1.flac", "track2.flac")))
    window.on_add_files(lambda current_album, *file: add_folder_signal.received([current_album, file]))
    window.display_album_screen(album)

    driver.add_tracks_in_folder()
    driver.check(add_folder_signal)


def test_signals_when_export_menu_item_clicked(driver):
    window = show_main_window(select_export_destination=lambda on_select, name: on_select(name + ".csv"))
    album = build.album(release_name="Honeycomb")
    export_signal = ValueMatcherProbe("export", contains(album, "Honeycomb.csv"))
    window.on_export(
        lambda current_album, destination: export_signal.received([current_album, destination]))
    window.display_album_screen(album)

    driver.export()
    driver.check(export_signal)


def test_signals_when_save_project_menu_item_clicked(driver):
    album = make_album()
    save_album_signal = ValueMatcherProbe("save", album)

    window = show_main_window(on_save_album=save_album_signal.received)
    window.display_album_screen(album)

    driver.save()
    driver.check(save_album_signal)


def test_signals_when_about_qt_menu_item_clicked(driver):
    about_qt_signal = ValueMatcherProbe("about Qt")

    _ = show_main_window(on_about_qt=lambda pressed: about_qt_signal.received())

    driver.about_qt()
    driver.check(about_qt_signal)


def test_signals_when_about_menu_item_clicked(driver):
    about_signal = ValueMatcherProbe("about")

    _ = show_main_window(on_about=lambda pressed: about_signal.received())

    driver.about()
    driver.check(about_signal)


def test_signals_when_online_help_menu_item_clicked(driver):
    online_help_signal = ValueMatcherProbe("online help", "http://blog.tagyourmusic.com/en")

    _ = show_main_window(on_online_help=online_help_signal.received)

    driver.help()
    driver.check(online_help_signal)


def test_signals_when_request_feature_menu_item_clicked(driver):
    request_feature_signal = ValueMatcherProbe("request feature",
                                               "mailto:support@tagyourmusic.com?subject=[TGiT] I want more!")

    _ = show_main_window(on_request_feature=request_feature_signal.received)

    driver.request_feature()
    driver.check(request_feature_signal)


def test_signals_when_register_menu_item_clicked(driver):
    register_signal = ValueMatcherProbe("register", "https://tagyourmusic.com/en")

    _ = show_main_window(on_register=register_signal.received)

    driver.register()
    driver.check(register_signal)


@pytest.mark.skipif(mac, reason="still unstable on Mac")
def test_signals_when_save_project_keyboard_shortcut_is_activated(driver):
    album = make_album()
    save_album_signal = ValueMatcherProbe("save", album)

    window = show_main_window(on_save_album=save_album_signal.received)
    window.display_album_screen(album)

    driver.save(using_shortcut=True)
    driver.check(save_album_signal)


def test_asks_for_confirmation_before_closing_project(driver):
    album = make_album()
    confirm_close_query = ValueMatcherProbe("confirm close")

    window = show_main_window(confirm_close=lambda **_: confirm_close_query.received(), on_close_album=ignore)
    window.display_album_screen(album)

    driver.close_project()
    driver.check(confirm_close_query)


def test_signals_when_project_closed(driver):
    album = make_album()
    close_album_signal = ValueMatcherProbe("close", album)

    window = show_main_window(confirm_close=lambda on_accept: on_accept(), on_close_album=close_album_signal.received)
    window.display_album_screen(album)

    driver.close_project()
    driver.check(close_album_signal)


@pytest.mark.skipif(mac, reason="still unstable on Mac")
def test_shows_confirmation_when_close_project_keyboard_shortcut_is_activated(driver):
    window = show_main_window()
    window.enable_project_actions(build.album())
    driver.close_project(using_shortcut=True)


def test_signals_when_settings_menu_item_clicked(driver):
    window = show_main_window()
    change_settings_signal = ValueMatcherProbe("change settings")
    window.on_settings(lambda checked: change_settings_signal.received())

    driver.settings()
    driver.check(change_settings_signal)


def test_navigates_to_project_edition_page_item_when_menu_item_is_clicked(driver):
    window = show_main_window()
    album = build.album()
    window.display_album_screen(album)

    driver.navigate_to_project_page()
    project_screen(driver).is_showing_project_edition_page()


def test_adds_track_menu_item_when_adding_a_track_to_the_project(driver):
    window = show_main_window()
    album = build.album()
    window.display_album_screen(album)
    album.add_track(build.track(track_title="Chevere!"))

    driver.shows_track_menu_item(title="Chevere!", track_number=1)


def test_updates_track_menu_item_when_track_name_changes(driver):
    window = show_main_window()
    album = build.album()
    window.display_album_screen(album)
    album.add_track(build.track(track_title="Chevere!"))
    album.tracks[0].track_title = "Zumbar"

    driver.shows_track_menu_item(title="Zumbar", track_number=1)


def test_updates_track_menu_item_when_tracks_change_order(driver):
    window = show_main_window()
    album = build.album()
    window.display_album_screen(album)
    album.add_track(build.track(track_title="Chevere!"))
    album.add_track(build.track(track_title="Zumbar"))

    album.move_track(1, 0)

    driver.shows_track_menu_item(title="Zumbar", track_number=1)
    driver.shows_track_menu_item(title="Chevere!", track_number=2)


def test_removes_track_menu_item_when_removing_a_track_from_the_project(driver):
    window = show_main_window()
    album = build.album()
    window.display_album_screen(album)

    album.add_track(build.track(track_title="Chevere!"))
    album.remove_track(0)

    driver.does_not_show_menu_item(title="Chevere!", track_number=1)


def test_displays_track_menu_item_when_loading_an_existing_project(driver):
    window = show_main_window()
    album = build.album(tracks=[build.track(track_title="Chevere!"), build.track(track_title="Zumbar")])
    window.display_album_screen(album)

    driver.shows_track_menu_item(title="Chevere!", track_number=1)
    driver.shows_track_menu_item(title="Zumbar", track_number=2)


def test_removes_track_menu_item_when_closing_an_project(driver):
    window = show_main_window()
    album = build.album(tracks=[build.track(track_title="Chevere!"), build.track(track_title="Zumbar")])
    window.display_album_screen(album)

    window.display_startup_screen()

    album = build.album()
    window.display_album_screen(album)

    driver.does_not_show_menu_item(title="Chevere!", track_number=1)
    driver.does_not_show_menu_item(title="Zumbar", track_number=2)


def test_navigates_to_track_page_when_menu_item_is_clicked(driver):
    window = show_main_window()
    album = build.album()
    window.display_album_screen(album)
    album.add_track(build.track(track_title="Chevere!"))
    album.add_track(build.track(track_title="Zumbar"))
    album.add_track(build.track(track_title="Salsa Coltrane"))

    driver.navigate_to_track_page(title="Salsa Coltrane", track_number=3)
    project_screen(driver).is_showing_track_edition_page(3)


def test_closes_main_widget_when_changing_page(driver):
    window = show_main_window()
    album = build.album()

    screen = startup_screen(driver).widget()
    window.display_album_screen(album)
    no_startup_screen(driver).exists()
    screen.is_closed()

    screen = project_screen(driver).widget()
    window.display_startup_screen()
    no_album_screen(driver).exists()
    screen.is_closed()


def test_warn_user_if_save_fails(driver):
    save_failed_signal = ValueMatcherProbe("save album failed", instance_of(OSError))
    album = make_album()

    window = show_main_window(on_save_album=_raise_os_error("Save failed"), show_save_error=save_failed_signal.received)
    window.display_album_screen(album)

    driver.save()
    driver.check(save_failed_signal)


def test_warn_user_if_export_fails(driver):
    def on_export(callback, _):
        callback("...")

    export_failed_signal = ValueMatcherProbe("export failed", instance_of(OSError))
    album = make_album()

    window = show_main_window(on_export=_raise_os_error("Export failed"),
                              show_export_error=export_failed_signal.received,
                              select_export_destination=on_export)
    window.display_album_screen(album)

    driver.export()
    driver.check(export_failed_signal)


def test_signals_when_sign_in_menu_item_clicked(driver):
    sign_in_signal = ValueMatcherProbe("sign in")

    _ = show_main_window(on_sign_in=sign_in_signal.received)

    driver.sign_in()
    driver.check(sign_in_signal)


def test_displays_the_logged_user(driver):
    window = show_main_window()
    window.user_signed_in(User(email="test@example.com"))

    driver.is_signed_in_as("test@example.com")


def test_signals_when_sign_out_menu_item_clicked(driver):
    sign_out_signal = ValueMatcherProbe("sign out")

    window = show_main_window(on_sign_out=sign_out_signal.received)
    window.user_signed_in(User(email="test@example.com"))

    driver.sign_out()
    driver.check(sign_out_signal)


def test_hides_the_logged_user_menu_item(driver):
    window = show_main_window()
    window.user_signed_in(User(email="test@example.com"))
    window.user_signed_out(None)

    driver.is_signed_out()


def test_signals_when_transmit_to_soproq_menu_item_clicked(driver):
    album = build.album(release_name="Honeycomb")
    transmit_signal = MultiValueMatcherProbe("transmit to soproq", contains(album, "Honeycomb.xlsx"))

    window = show_main_window(select_save_as_destination=lambda on_select, name: on_select(name + ".xlsx"),
                              on_transmit_to_soproq=transmit_signal.received)
    window.display_album_screen(album)

    driver.transmit_to_soproq()
    driver.check(transmit_signal)
