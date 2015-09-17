# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from hamcrest import contains
import pytest

from authentication_error import AuthenticationError
from cute.matchers import named
from cute.probes import ValueMatcherProbe, MultiValueMatcherProbe
from cute.widgets import window
from drivers.sign_in_dialog_driver import SignInDialogDriver
from ui.sign_in_dialog import SignInDialog

ignore = lambda *_: None


def show_dialog(on_successful_authentication=ignore, authenticate=ignore):
    dialog = SignInDialog(authenticate=authenticate)
    dialog.setAttribute(Qt.WA_DeleteOnClose, False)
    dialog.sign_in(on_successful_authentication)
    return dialog


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    dialog_driver = SignInDialogDriver(window(SignInDialog, named("sign_in_dialog")), prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def test_signals_with_authentication_result_when_authentication_is_successful(driver):
    authentication_successful_signal = ValueMatcherProbe("authentication", "token")

    _ = show_dialog(on_successful_authentication=authentication_successful_signal.received,
                    authenticate=lambda *_: "token")

    driver.enter_credentials("jfalardeau@pyxis-tech.com", "passw0rd")
    driver.check(authentication_successful_signal)


def test_calls_authenticate_with_credentials(driver):
    authentication_successful_signal = MultiValueMatcherProbe("authentication",
                                                              contains("jfalardeau@pyxis-tech.com", "passw0rd"))

    _ = show_dialog(authenticate=authentication_successful_signal.received)

    driver.enter_credentials("jfalardeau@pyxis-tech.com", "passw0rd")
    driver.check(authentication_successful_signal)


def test_displays_error_message_when_authentication_is_not_successful(driver):
    def authenticate(_, __):
        raise AuthenticationError()

    _ = show_dialog(authenticate=authenticate)

    driver.enter_credentials("jfalardeau@pyxis-tech.com", "passw0rd")
    driver.shows_authentication_failed_message()
