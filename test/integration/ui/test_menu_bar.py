# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow
import pytest

from cute.finders import WidgetIdentity
from cute.prober import EventProcessingProber
from cute.probes import ValueMatcherProbe
from cute.robot import Robot
from test.drivers import MenuBarDriver
from test.integration.ui import show_widget
from test.util import builders as build
from tgit.ui.menu_bar import MenuBar


@pytest.yield_fixture()
def menu_bar(qt):
    main_window = QMainWindow()
    menu = MenuBar(main_window)
    show_widget(main_window)
    yield menu


@pytest.yield_fixture()
def driver(menu_bar):
    driver = MenuBarDriver(WidgetIdentity(menu_bar), EventProcessingProber(), Robot())
    yield driver
    driver.close()


def test_album_menu_is_initially_disabled(driver):
    driver.has_disabled_album_actions()


def test_signals_when_add_files_menu_item_clicked(menu_bar, driver):
    album = build.album()
    add_files_signal = ValueMatcherProbe('add files', album)
    menu_bar.add_files.connect(add_files_signal.received)
    menu_bar.albumCreated(album)

    driver.add_files()
    driver.check(add_files_signal)


def test_signals_when_add_folder_menu_item_clicked(menu_bar, driver):
    album = build.album()
    add_folder_signal = ValueMatcherProbe('add folder', album)
    menu_bar.add_folder.connect(add_folder_signal.received)
    menu_bar.albumCreated(album)

    driver.add_folder()
    driver.check(add_folder_signal)


def testSignalsWhenExportMenuItemClicked(menu_bar, driver):
    album = build.album()
    export_album_signal = ValueMatcherProbe('export', album)
    menu_bar.export.connect(export_album_signal.received)
    menu_bar.albumCreated(album)

    driver.export()
    driver.check(export_album_signal)


def testSignalsWhenSettingsMenuItemClicked(menu_bar, driver):
    change_settings_signal = ValueMatcherProbe('change settings')
    menu_bar.settings.connect(change_settings_signal.received)

    driver.settings()
    driver.check(change_settings_signal)