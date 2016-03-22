import pytest
from hamcrest import contains

from cute import platforms
from cute.matchers import named
from cute.probes import MultiValueMatcherProbe
from cute.widgets import window
from test.drivers.sign_in_dialog_driver import SignInDialogDriver
from test.integration.ui import ignore
from test.util.builders import make_anonymous_session
from tgit.auth import Login
from tgit.ui.dialogs.sign_in_dialog import SignInDialog, open_sign_in_dialog

pytestmark = pytest.mark.ui

DISPLAY_DELAY = 250 if platforms.mac else 0


def open_dialog(on_sign_in=ignore):
    return open_sign_in_dialog(Login(make_anonymous_session()), on_sign_in=on_sign_in, delete_on_close=False)


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    dialog_driver = SignInDialogDriver(window(SignInDialog, named("sign_in_dialog")), prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def test_disables_authentication_until_an_email_is_entered(driver):
    _ = open_dialog()

    driver.has_disabled_authentication()
    driver.pause(DISPLAY_DELAY)
    driver.enter_email("email")
    driver.has_enabled_authentication()


def test_signals_authentication_attempt_with_credentials(driver):
    sign_in_signal = MultiValueMatcherProbe("credentials", contains("jfalardeau@pyxis-tech.com", "passw0rd"))

    _ = open_dialog(on_sign_in=sign_in_signal.received)

    driver.pause(DISPLAY_DELAY)
    driver.sign_in_with("jfalardeau@pyxis-tech.com", "passw0rd")
    driver.check(sign_in_signal)


def test_displays_progress_indicator_and_disable_authentication_when_login_in_progress(driver):
    dialog = open_dialog()
    driver.pause(DISPLAY_DELAY)

    driver.has_stopped_progress_indicator()

    driver.enter_email("test@example.com")
    dialog.login_in_progress()
    driver.is_showing_progress_indicator()
    driver.has_disabled_authentication()


def test_stops_progress_indicator_and_displays_error_message_when_login_fails(driver):
    dialog = open_dialog()
    driver.pause(DISPLAY_DELAY)

    driver.enter_email("test@example.com")
    dialog.login_in_progress()
    driver.is_showing_progress_indicator()

    dialog.login_failed()
    driver.has_stopped_progress_indicator()
    driver.shows_authentication_failed_message()
    driver.has_enabled_authentication()


def test_stops_progress_indicator_and_accepts_dialog_when_login_succeeds(driver):
    dialog = open_dialog()
    driver.pause(DISPLAY_DELAY)

    dialog.login_in_progress()
    driver.is_showing_progress_indicator()

    dialog.login_succeeded()
    driver.has_stopped_progress_indicator()
    driver.is_hidden()
