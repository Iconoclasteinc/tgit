import types

from PyQt5.QtCore import Qt
from hamcrest import contains, instance_of
import pytest
import requests

from cute.matchers import named
from cute.probes import ValueMatcherProbe, MultiValueMatcherProbe
from cute.widgets import window
from test.drivers.isni_lookup_dialog_driver import IsniLookupDialogDriver
from tgit.identity import IdentityCard
from tgit.ui.dialogs.isni_lookup_dialog import ISNILookupDialog, make_isni_lookup_dialog

pytestmark = pytest.mark.ui


def show_dialog(query=None, **handlers):
    dialog = make_isni_lookup_dialog(parent=None, **handlers)
    dialog.setAttribute(Qt.WA_DeleteOnClose, False)
    dialog.lookup(query)
    return dialog


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    dialog_driver = IsniLookupDialogDriver(window(ISNILookupDialog, named("isni_lookup_dialog")), prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def test_hides_error_messages_by_default(driver):
    _ = show_dialog()
    driver.shows_no_result_message(visible=False)
    driver.shows_connection_error_message(visible=False)


def test_signals_lookup_on_display(driver):
    signal = MultiValueMatcherProbe("lookup ISNI", contains("Joel Miller",
                                                            instance_of(types.FunctionType),
                                                            instance_of(types.FunctionType)))
    _ = show_dialog("Joel Miller", on_isni_lookup=signal.received)
    driver.shows_results_list(enabled=False)
    driver.check(signal)


def test_signals_lookup_on_click(driver):
    signal = MultiValueMatcherProbe("lookup ISNI", contains("Joel Miller",
                                                            instance_of(types.FunctionType),
                                                            instance_of(types.FunctionType)))
    _ = show_dialog(on_isni_lookup=signal.received)

    driver.lookup("Joel Miller")
    driver.check(signal)


def test_displays_lookup_results(driver):
    _ = show_dialog(on_isni_lookup=lambda _, success, __: success(
        [IdentityCard(id="0000000123456789",
                      type=IdentityCard.INDIVIDUAL,
                      firstName="Joel",
                      lastName="Miller",
                      dateOfBirth="1969",
                      dateOfDeath="2100",
                      works=[{"title": "Chevere!"}]),
         IdentityCard(id="9876543210000000",
                      type=IdentityCard.INDIVIDUAL,
                      firstName="John",
                      lastName="Roney",
                      dateOfBirth="1700",
                      dateOfDeath="2500",
                      works=[{"title": "Zumbar"}])]))

    driver.lookup("Joel Miller")
    driver.displays_result("Joel Miller", "1969", "2100", "Chevere!")
    driver.displays_result("John Roney", "1700", "2500", "Zumbar")


def test_displays_only_last_lookup_results(driver):
    def on_lookup(query, success, _):
        if query == "Joel Miller":
            success([IdentityCard(id="0000000123456789",
                                  type=IdentityCard.INDIVIDUAL,
                                  firstName="Joel",
                                  lastName="Miller",
                                  dateOfBirth="1969",
                                  dateOfDeath="2100",
                                  works=[{"title": "Chevere!"}])])
        else:
            success([IdentityCard(id="9876543210000000",
                                  type=IdentityCard.INDIVIDUAL,
                                  firstName="John",
                                  lastName="Roney",
                                  dateOfBirth="1700",
                                  dateOfDeath="2500",
                                  works=[{"title": "Zumbar"}])])

    _ = show_dialog(on_isni_lookup=on_lookup)

    driver.lookup("Joel Miller")
    driver.lookup("John Roney")
    driver.displays_result("John Roney", "1700", "2500", "Zumbar")


def test_signals_selected_identity(driver):
    signal = ValueMatcherProbe("lookup ISNI", "0000000123456789")

    _ = show_dialog(on_isni_selected=signal.received,
                    on_isni_lookup=lambda _, success, __:
                    success([IdentityCard(id="0000000123456789",
                                          type=IdentityCard.INDIVIDUAL,
                                          firstName="Joel",
                                          lastName="Miller",
                                          dateOfBirth="1969",
                                          dateOfDeath="2100",
                                          works=[{"title": "Chevere!"}])]))

    driver.lookup("Joel Miller")
    driver.select_identity("Joel Miller")
    driver.accept()
    driver.check(signal)


def test_disables_ok_button_by_default(driver):
    _ = show_dialog()
    driver.has_ok_button_disabled()


def test_disables_ok_button_on_new_search(driver):
    _ = show_dialog(on_isni_lookup=lambda _, success, __:
    success([IdentityCard(id="0000000123456789",
                          type=IdentityCard.INDIVIDUAL,
                          firstName="Joel",
                          lastName="Miller",
                          dateOfBirth="1969",
                          dateOfDeath="2100",
                          works=[{"title": "Chevere!"}])]))

    driver.lookup("Joel Miller")
    driver.select_identity("Joel Miller")
    driver.lookup("Joel Miller")
    driver.has_ok_button_disabled()


def test_enables_lookup_button_when_text_is_entered(driver):
    _ = show_dialog()

    driver.has_lookup_button_enabled(enabled=False)
    driver.change_query("Joel Miller")
    driver.has_lookup_button_enabled()


def test_displays_no_result_message(driver):
    _ = show_dialog(on_isni_lookup=lambda _, success, __: success([]))

    driver.lookup("Joel Miller")
    driver.shows_no_result_message()
    driver.lookup("John Roney")


def test_hides_no_result_message(driver):
    def on_isni_lookup(query, success, _):
        if query == "Joel Miller":
            success([])
        else:
            success([IdentityCard(id="0000000123456789",
                                  type=IdentityCard.INDIVIDUAL,
                                  firstName="Joel",
                                  lastName="Miller",
                                  dateOfBirth="1969",
                                  dateOfDeath="2100",
                                  works=[{"title": "Chevere"}])])

    _ = show_dialog(on_isni_lookup=on_isni_lookup)

    driver.lookup("Joel Miller")
    driver.shows_no_result_message()
    driver.lookup("John Roney")
    driver.shows_no_result_message(visible=False)


def test_displays_connection_error_message(driver):
    _ = show_dialog(on_isni_lookup=lambda _, __, error: error(requests.ConnectionError()))

    driver.lookup("Joel Miller")
    driver.shows_connection_error_message()


def test_hides_connection_error_message(driver):
    def on_isni_lookup(query, success, error):
        if query == "Joel Miller":
            error(requests.ConnectionError())
        else:
            success([IdentityCard(id="0000000123456789",
                                  type=IdentityCard.INDIVIDUAL,
                                  firstName="Joel",
                                  lastName="Miller",
                                  dateOfBirth="1969",
                                  dateOfDeath="2100",
                                  works=[{"title": "Chevere"}])])

    _ = show_dialog(on_isni_lookup=on_isni_lookup)

    driver.lookup("Joel Miller")
    driver.shows_connection_error_message()
    driver.lookup("John Roney")
    driver.shows_connection_error_message(visible=False)
