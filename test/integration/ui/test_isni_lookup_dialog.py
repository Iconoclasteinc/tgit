from hamcrest import has_property
import pytest
import requests

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers.isni_lookup_dialog_driver import IsniLookupDialogDriver
from tgit.identity import IdentityCard, IdentityLookup
from tgit.ui.dialogs.isni_lookup_dialog import ISNILookupDialog, make_isni_lookup_dialog

pytestmark = pytest.mark.ui


def show_dialog(query=None, identity_lookup=IdentityLookup(), **handlers):
    dialog = make_isni_lookup_dialog(parent=None,
                                     identity_lookup=identity_lookup,
                                     delete_on_close=False,
                                     **handlers)
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
    signal = ValueMatcherProbe("lookup ISNI", "Joel Miller")
    _ = show_dialog("Joel Miller", on_lookup=signal.received)
    driver.shows_results_list(enabled=False)
    driver.check(signal)


def test_signals_lookup_on_click(driver):
    signal = ValueMatcherProbe("lookup ISNI", "Joel Miller")
    _ = show_dialog(on_lookup=signal.received)

    driver.lookup("Joel Miller")
    driver.check(signal)


def test_displays_lookup_results(driver):
    dialog = show_dialog()
    dialog.display_identities([IdentityCard(id="0000000123456789",
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
    dialog.display_identities([IdentityCard(id="0000000123456789",
                                            type=IdentityCard.INDIVIDUAL,
                                            firstName="Joel",
                                            lastName="Miller",
                                            dateOfBirth="1969",
                                            dateOfDeath="2100",
                                            works=[{"title": "Chevere!"}])])
    dialog.display_identities([IdentityCard(id="9876543210000000",
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
    identity_lookup.success.subscribe(signal.received)

    dialog = show_dialog(identity_lookup=identity_lookup)
    dialog.display_identities([IdentityCard(id="0000000123456789",
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


def test_disables_ok_button_on_new_search(driver):
    identities = [IdentityCard(id="0000000123456789",
                               type=IdentityCard.INDIVIDUAL,
                               firstName="Joel",
                               lastName="Miller",
                               dateOfBirth="1969",
                               dateOfDeath="2100",
                               works=[{"title": "Chevere!"}])]

    dialog = show_dialog()
    dialog.display_identities(identities)
    driver.select_identity("Joel Miller")
    dialog.display_identities(identities)
    driver.has_ok_button_disabled()


def test_displays_no_result_message(driver):
    dialog = show_dialog()
    dialog.display_identities([])
    driver.shows_no_result_message()


def test_hides_no_result_message(driver):
    dialog = show_dialog()
    dialog.display_identities([])
    driver.shows_no_result_message()
    dialog.display_identities([IdentityCard(id="0000000123456789",
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
    dialog.display_identities([IdentityCard(id="0000000123456789",
                                            type=IdentityCard.INDIVIDUAL,
                                            firstName="Joel",
                                            lastName="Miller",
                                            dateOfBirth="1969",
                                            dateOfDeath="2100",
                                            works=[{"title": "Chevere!"}])])
    driver.shows_connection_error_message(visible=False)
