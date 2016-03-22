import pytest
from PyQt5.QtWidgets import QMessageBox
from hamcrest import contains_string

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import QMessageBoxDriver, window
from test.drivers.about_dialog_driver import AboutDialogDriver
from tgit import platforms
from tgit.ui.dialogs.about_dialog import AboutDialog
from tgit.ui.dialogs.message_boxes import MessageBoxes

pytestmark = pytest.mark.ui

DISPLAY_DELAY = 200 if platforms.mac else 0


@pytest.fixture()
def driver(qt, prober, automaton):
    return QMessageBoxDriver(window(QMessageBox, named("message_box")), prober, automaton)


@pytest.yield_fixture()
def about_tgit_driver(qt, prober, automaton):
    message_box_driver = AboutDialogDriver(window(AboutDialog, named("about_tgit_dialog")), prober, automaton)
    yield message_box_driver
    message_box_driver.close()


def messages(confirm_before_exiting=False):
    return MessageBoxes(confirm_before_exiting, get_parent=lambda: None)


def test_shows_isni_assignation_failed_message_with_details(driver):
    _ = messages().isni_assignation_failed(details="Details")
    driver.is_active()
    driver.shows_message("Could not assign an ISNI.")
    driver.shows_details("Details")
    driver.click_ok()


def test_shows_cheddar_connection_failed_message(driver):
    _ = messages().cheddar_connection_failed()
    driver.is_active()
    driver.shows_message("Unable to connect to the TGiT service.")
    driver.click_ok()


def test_shows_cheddar_authentication_failed_message(driver):
    _ = messages().cheddar_authentication_failed()
    driver.is_active()
    driver.shows_message("Could not authenticate you to the TGiT service.")
    driver.click_ok()


def test_shows_permission_denied_message(driver):
    _ = messages().permission_denied()
    driver.is_active()
    driver.shows_message("You don't have the required permission or you might have exceeded the limit of your plan.")
    driver.click_ok()


def test_shows_close_project_message(driver):
    _ = messages().close_project_confirmation()

    driver.is_active()
    driver.shows_message(contains_string("You are about to close the current project."))


def test_shows_restart_message(driver):
    _ = messages().restart_required()

    driver.is_active()
    driver.shows_message(contains_string("You need to restart TGiT for changes to take effect."))


def test_shows_overwrite_project_confirmation_message(driver):
    _ = messages().overwrite_project_confirmation()

    driver.is_active()
    driver.shows_message(contains_string("This project already exists."))


def test_signals_when_confirmed(driver):
    accept_signal = ValueMatcherProbe("accept confirmation")
    _ = messages().close_project_confirmation(on_accept=accept_signal.received)

    driver.is_active()
    driver.pause(DISPLAY_DELAY)
    driver.click_yes()
    driver.check(accept_signal)


def test_shows_load_project_failed_message(driver):
    _ = messages().load_project_failed(Exception())

    driver.is_active()
    driver.shows_message(contains_string("The project file you selected cannot be loaded."))


def test_shows_save_project_failed_message(driver):
    _ = messages().save_project_failed(Exception())

    driver.is_active()
    driver.shows_message(contains_string("Your project file could not be saved."))


def test_shows_export_failed_message(driver):
    _ = messages().export_failed(Exception())

    driver.is_active()
    driver.shows_message("Could not export your project.")


def test_shows_soproq_default_values_message(driver):
    _ = messages().warn_soproq_default_values()

    driver.is_active()
    driver.shows_message("SOPROQ declaration file was generated with default values.")


def test_shows_about_message(about_tgit_driver):
    _ = messages().about_tgit()

    about_tgit_driver.is_active()
