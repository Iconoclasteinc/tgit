import pytest
from hamcrest import contains

from cute.matchers import named
from cute.probes import MultiValueMatcherProbe
from cute.widgets import window
from test.drivers.sign_in_dialog_driver import SignInDialogDriver
from test.integration.ui import ignore
from test.util.builders import make_anonymous_session
from tgit.auth import Login
from tgit.ui.dialogs.sign_in_dialog import SignInDialog, open_sign_in_dialog

pytestmark = pytest.mark.ui


def open_dialog(on_sign_in=ignore):
    return open_sign_in_dialog(parent=None,
                               login=Login(make_anonymous_session()),
                               on_sign_in=on_sign_in,
                               delete_on_close=False)


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    dialog_driver = SignInDialogDriver(window(SignInDialog, named("sign_in_dialog")), prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def test_signals_authentication_attempt_with_credentials(driver):
    sign_in_signal = MultiValueMatcherProbe("credentials", contains("jfalardeau@pyxis-tech.com", "passw0rd"))

    _ = open_dialog(on_sign_in=sign_in_signal.received)

    driver.is_active()
    driver.sign_in_with("jfalardeau@pyxis-tech.com", "passw0rd")
    driver.check(sign_in_signal)


def test_displays_progress_indicator_when_login_in_progress(driver):
    dialog = open_dialog()

    driver.has_stopped_progress_indicator()
    dialog.login_in_progress()
    driver.has_started_progress_indicator()


def test_stops_progress_indicator_and_displays_error_message_when_login_fails(driver):
    dialog = open_dialog()

    dialog.login_failed()
    driver.has_stopped_progress_indicator()
    driver.shows_authentication_failed_message()


def test_stops_progress_indicator_and_accepts_dialog_when_login_succeeds(driver):
    dialog = open_dialog()

    dialog.login_succeeded()
    driver.has_stopped_progress_indicator()
    driver.is_hidden()
