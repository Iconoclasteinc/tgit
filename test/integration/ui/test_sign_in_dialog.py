# -*- coding: utf-8 -*-
import pytest
from PyQt5.QtCore import Qt
from hamcrest import contains

from cute.matchers import named
from cute.probes import MultiValueMatcherProbe
from cute.widgets import window
from test.drivers.sign_in_dialog_driver import SignInDialogDriver
from tgit.authentication_error import AuthenticationError
from tgit.ui.sign_in_dialog import SignInDialog

ignore = lambda *_: None


def show_dialog(on_sign_in=ignore):
    dialog = SignInDialog()
    dialog.setAttribute(Qt.WA_DeleteOnClose, False)
    dialog.sign_in(on_sign_in)
    return dialog


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    dialog_driver = SignInDialogDriver(window(SignInDialog, named("sign_in_dialog")), prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def test_calls_authenticate_with_credentials(driver):
    sign_in_signal = MultiValueMatcherProbe("authentication", contains("jfalardeau@pyxis-tech.com", "passw0rd"))

    _ = show_dialog(on_sign_in=sign_in_signal.received)
    driver.is_active()

    driver.enter_credentials("jfalardeau@pyxis-tech.com", "passw0rd")
    driver.check(sign_in_signal)


def test_displays_error_message_when_authentication_is_not_successful(driver):
    def authenticate(*_):
        raise AuthenticationError()

    _ = show_dialog(on_sign_in=authenticate)

    driver.is_active()
    driver.enter_credentials("jfalardeau@pyxis-tech.com", "passw0rd")
    driver.shows_authentication_failed_message()
