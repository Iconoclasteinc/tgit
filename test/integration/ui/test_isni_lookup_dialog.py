import pytest
import requests
from hamcrest import has_property

from cute import platforms
from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers.isni_lookup_dialog_driver import IsniLookupDialogDriver
from test.integration.ui import ignore
from tgit.identity import IdentityCard, IdentityLookup
from tgit.ui.dialogs.isni_lookup_dialog import ISNILookupDialog, open_isni_lookup_dialog

pytestmark = pytest.mark.ui

DISPLAY_DELAY = 250 if platforms.mac else 0


def show_dialog(query=None, identity_lookup=IdentityLookup(), on_lookup=ignore):
    return open_isni_lookup_dialog(query, identity_lookup, on_lookup, delete_on_close=False)


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
    signal = ValueMatcherProbe("lookup ISNI", "Joel Miller")
    _ = show_dialog("Joel Miller", on_lookup=signal.received)
    driver.check(signal)


def test_signals_lookup_on_click(driver):
    signal = ValueMatcherProbe("lookup ISNI", "Joel Miller")
    _ = show_dialog(on_lookup=signal.received)

    driver.pause(DISPLAY_DELAY)
    driver.lookup("Joel Miller")
    driver.check(signal)


def test_displays_lookup_results(driver):
    dialog = show_dialog()
    dialog.lookup_successful([IdentityCard(id="0000000123456789",
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
                                           works=[{"title": "Zumbar"}])])

    driver.displays_result("Joel Miller", "1969", "2100", "Chevere!")
    driver.displays_result("John Roney", "1700", "2500", "Zumbar")


def test_displays_only_last_lookup_results(driver):
    dialog = show_dialog()
    dialog.lookup_successful([IdentityCard(id="0000000123456789",
                                           type=IdentityCard.INDIVIDUAL,
                                           firstName="Joel",
                                           lastName="Miller",
                                           dateOfBirth="1969",
                                           dateOfDeath="2100",
                                           works=[{"title": "Chevere!"}])])
    dialog.lookup_successful([IdentityCard(id="9876543210000000",
                                           type=IdentityCard.INDIVIDUAL,
                                           firstName="John",
                                           lastName="Roney",
                                           dateOfBirth="1700",
                                           dateOfDeath="2500",
                                           works=[{"title": "Zumbar"}])])
    driver.displays_result("John Roney", "1700", "2500", "Zumbar")


def test_signals_selected_identity(driver):
    signal = ValueMatcherProbe("lookup ISNI", has_property("id", "0000000123456789"))

    identity_lookup = IdentityLookup()
    identity_lookup.on_success.subscribe(signal.received)

    dialog = show_dialog(identity_lookup=identity_lookup)

    driver.pause(DISPLAY_DELAY)
    dialog.lookup_successful([IdentityCard(id="0000000123456789",
                                           type=IdentityCard.INDIVIDUAL,
                                           firstName="Joel",
                                           lastName="Miller",
                                           dateOfBirth="1969",
                                           dateOfDeath="2100",
                                           works=[{"title": "Chevere!"}])])
    driver.select_identity("Joel Miller")
    driver.accept()
    driver.check(signal)


def test_disables_ok_button_by_default(driver):
    _ = show_dialog()
    driver.has_ok_button_disabled()


def test_disables_ok_button_when_lookup_in_progress(driver):
    dialog = show_dialog()
    dialog.lookup_successful([IdentityCard(id="0000000123456789",
                                           type=IdentityCard.INDIVIDUAL,
                                           firstName="Joel",
                                           lastName="Miller",
                                           dateOfBirth="1969",
                                           dateOfDeath="2100",
                                           works=[{"title": "Chevere!"}])])
    dialog.lookup_in_progress()
    driver.has_ok_button_disabled()


def test_displays_no_result_message(driver):
    dialog = show_dialog()
    dialog.lookup_successful([])
    driver.shows_no_result_message()


def test_hides_no_result_message(driver):
    dialog = show_dialog()
    dialog.lookup_successful([])
    driver.shows_no_result_message()
    dialog.lookup_successful([IdentityCard(id="0000000123456789",
                                           type=IdentityCard.INDIVIDUAL,
                                           firstName="Joel",
                                           lastName="Miller",
                                           dateOfBirth="1969",
                                           dateOfDeath="2100",
                                           works=[{"title": "Chevere!"}])])
    driver.shows_no_result_message(visible=False)


def test_displays_connection_error_message(driver):
    dialog = show_dialog()
    dialog.lookup_failed(requests.ConnectionError())
    driver.shows_connection_error_message()


def test_hides_connection_error_message(driver):
    dialog = show_dialog()
    dialog.lookup_failed(requests.ConnectionError())
    driver.shows_connection_error_message()
    dialog.lookup_successful([IdentityCard(id="0000000123456789",
                                           type=IdentityCard.INDIVIDUAL,
                                           firstName="Joel",
                                           lastName="Miller",
                                           dateOfBirth="1969",
                                           dateOfDeath="2100",
                                           works=[{"title": "Chevere!"}])])
    driver.shows_connection_error_message(visible=False)


def test_displays_progress_indicator_when_lookup_in_progress(driver):
    dialog = show_dialog()

    driver.has_stopped_progress_indicator()
    dialog.lookup_in_progress()
    driver.is_showing_progress_indicator()


def test_stops_progress_indicator_on_lookup_success(driver):
    dialog = show_dialog()

    dialog.lookup_in_progress()
    driver.is_showing_progress_indicator()

    dialog.lookup_successful([])
    driver.has_stopped_progress_indicator()


def test_stops_progress_indicator_on_lookup_failure(driver):
    dialog = show_dialog()

    dialog.lookup_in_progress()
    driver.is_showing_progress_indicator()

    dialog.lookup_failed("")
    driver.has_stopped_progress_indicator()


def test_disables_result_list_when_lookup_in_progress(driver):
    dialog = show_dialog()

    driver.shows_results_list()
    dialog.lookup_in_progress()
    driver.shows_results_list(enabled=False)
