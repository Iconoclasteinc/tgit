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


def test_displays_error_message_when_authentication_fails(driver):
    dialog = open_dialog()

    dialog.authentication_failed()
    driver.shows_authentication_failed_message()


def test_accepts_dialog_when_authentication_succeeds(driver):
    dialog = open_dialog()

    dialog.authentication_succeeded()
    driver.is_hidden()
