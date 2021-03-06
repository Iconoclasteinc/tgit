# -*- coding: utf-8 -*-
import pytest
from flexmock import flexmock
from hamcrest import assert_that, equal_to

from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.ui import ignore, show_, close_
from testing.builders import make_album
from testing.drivers import IsniLookupDialogDriver
from tgit.identity import Identities
from tgit.identity import IdentityCard, IdentitySelection
from tgit.ui.dialogs.isni_lookup_dialog import ISNILookupDialog, make_isni_lookup_dialog

pytestmark = pytest.mark.ui


def show_dialog(query=None, selection=IdentitySelection(make_album(), ""), on_lookup=ignore, on_assign=ignore):
    dialog = make_isni_lookup_dialog(query, selection, on_lookup, on_assign, delete_on_close=False)
    show_(dialog)
    return dialog


@pytest.yield_fixture()
def driver(prober, automaton):
    dialog_driver = IsniLookupDialogDriver(window(ISNILookupDialog), prober, automaton)
    yield dialog_driver
    close_(dialog_driver)


def test_hides_error_messages_by_default(driver):
    _ = show_dialog()
    driver.shows_no_result_message(visible=False)
    driver.shows_connection_error_message(visible=False)
    driver.shows_permission_denied_message(visible=False)


def test_signals_lookup_on_display(driver):
    signal = ValueMatcherProbe("lookup ISNI", "Joel Miller")
    _ = show_dialog("Joel Miller", on_lookup=signal.received)
    driver.check(signal)


def test_signals_lookup_on_click(driver):
    signal = ValueMatcherProbe("lookup ISNI", "Joel Miller")
    _ = show_dialog(on_lookup=signal.received)

    driver.lookup("Joel Miller")
    driver.check(signal)


def test_displays_lookup_results(driver):
    dialog = show_dialog()
    dialog.lookup_successful(Identities("2", [joel_miller(), john_roney()]))

    driver.displays_result("Joel Miller", "1969", "2100", "Chevere!")
    driver.displays_result("John Roney", "1700", "2500", "Zumbar")
    driver.displays_no_message()


def test_displays_refine_query_when_returning_more_than_the_displayed_results(driver):
    dialog = show_dialog()
    dialog.lookup_successful(Identities("1015", [joel_miller()]))

    driver.displays_refine_query_message("1015")


def test_displays_only_last_lookup_results(driver):
    dialog = show_dialog()
    dialog.lookup_successful(Identities("1", [joel_miller()]))
    dialog.lookup_successful(Identities("1", [john_roney()]))
    driver.displays_result("John Roney", "1700", "2500", "Zumbar")


def test_signals_selected_identity(driver):
    signal = ValueMatcherProbe("Selected identity")

    project = flexmock()
    project.should_receive("add_isni").with_args("Joel Miller", "0000000123456789").once()
    selection = IdentitySelection(project, "Joel Miller")
    selection.on_success.subscribe(signal.received)

    dialog = show_dialog(selection=selection)

    dialog.lookup_successful(Identities("1", [joel_miller()]))
    driver.select_identity("Joel Miller")
    driver.click_ok()
    driver.check(signal)


def test_signals_query_changed(driver):
    selection = IdentitySelection(make_album(), "John Roney")
    _ = show_dialog(selection=selection)

    driver.change_query("Joel Miller")
    assert_that(selection.query, equal_to("Joel Miller"), "The new query")


def test_disables_ok_button_by_default(driver):
    _ = show_dialog()
    driver.has_ok_button_disabled()


def test_disables_assignation_button_by_default(driver):
    _ = show_dialog()
    driver.shows_assignation_button(enabled=False)


def test_disables_assignation_button_after_successful_lookup(driver):
    dialog = show_dialog()
    driver.shows_assignation_button(enabled=False)
    dialog.lookup_successful(Identities("1", [joel_miller()]))
    driver.shows_assignation_button(enabled=False)
    dialog.lookup_successful([])
    driver.shows_assignation_button()


def test_signals_assignation(driver):
    signal = ValueMatcherProbe("assign ISNI")
    dialog = show_dialog(on_assign=signal.received)
    dialog.lookup_successful([])
    driver.assign()
    driver.check(signal)


def test_disables_ok_button_when_lookup_in_progress(driver):
    dialog = show_dialog()
    dialog.lookup_successful(Identities("1", [joel_miller()]))
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
    dialog.lookup_successful(Identities("1", [joel_miller()]))
    driver.shows_no_result_message(visible=False)


def test_displays_connection_error_message(driver):
    dialog = show_dialog()
    dialog.connection_failed()
    driver.shows_connection_error_message()


def test_hides_connection_error_message(driver):
    dialog = show_dialog()
    dialog.connection_failed()
    driver.shows_connection_error_message()
    dialog.lookup_successful(Identities("1", [joel_miller()]))
    driver.shows_connection_error_message(visible=False)


def test_displays_permission_denied_message(driver):
    dialog = show_dialog()
    dialog.permission_denied()
    driver.shows_permission_denied_message()


def test_hides_permission_denied_message(driver):
    dialog = show_dialog()
    dialog.permission_denied()
    driver.shows_permission_denied_message()
    dialog.lookup_successful(Identities("1", [joel_miller()]))
    driver.shows_permission_denied_message(visible=False)


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


def test_stops_progress_indicator_on_connection_failure(driver):
    dialog = show_dialog()

    dialog.lookup_in_progress()
    driver.is_showing_progress_indicator()

    dialog.connection_failed()
    driver.has_stopped_progress_indicator()


def test_disables_result_list_when_lookup_in_progress(driver):
    dialog = show_dialog()

    driver.shows_results_list()
    dialog.lookup_in_progress()
    driver.shows_results_list(enabled=False)


def test_closes_dialog_on_assignation_success(driver):
    dialog = show_dialog()

    dialog.selection_successful()
    driver.is_hidden()


def joel_miller():
    return IdentityCard(id="0000000123456789",
                        type=IdentityCard.INDIVIDUAL,
                        firstName="Joel",
                        lastName="Miller",
                        dateOfBirth="1969",
                        dateOfDeath="2100",
                        works=[{"title": "Chevere!"}])


def john_roney():
    return IdentityCard(id="9876543210000000",
                        type=IdentityCard.INDIVIDUAL,
                        firstName="John",
                        lastName="Roney",
                        dateOfBirth="1700",
                        dateOfDeath="2500",
                        works=[{"title": "Zumbar"}])
