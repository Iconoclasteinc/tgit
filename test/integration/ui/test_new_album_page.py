import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers.new_project_page_driver import NewProjectPageDriver
from tgit.ui.pages.new_project_page import NewProjectPage, make_new_project_page

pytestmark = pytest.mark.ui


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    page_driver = NewProjectPageDriver(window(NewProjectPage, named("new_project_page")), prober, automaton)
    yield page_driver
    page_driver.close()


def ignore(*_, **__):
    pass


def always(on_accept):
    on_accept()


def no(*_):
    return False


def yes(*_):
    return True


def show_page(page_driver, of_type="mp3", select_project_location=ignore, select_track=ignore, confirm_overwrite=always,
              project_exists=no, on_create_project=ignore):
    page = make_new_project_page(select_location=select_project_location,
                                 select_track=select_track,
                                 confirm_overwrite=confirm_overwrite,
                                 check_project_exists=project_exists,
                                 on_create_project=on_create_project)
    page.project_type = of_type
    page_driver.show()
    return page


@pytest.mark.parametrize("using_shortcut", [False, True])
def test_signals_project_creation(driver, using_shortcut):
    show_page(driver, of_type="flac", on_create_project=lambda *args: create_project_signal.received(args))
    create_project_signal = ValueMatcherProbe("new project", ("flac", "Honeycomb", "~Documents", "track.mp3"))

    driver.create_project("Honeycomb", "~Documents", import_from="track.mp3", using_shortcut=using_shortcut)
    driver.check(create_project_signal)


@pytest.mark.parametrize("using_shortcut", [False, True])
def test_signals_project_creation_cancellation(driver, using_shortcut):
    cancel_creation_signal = ValueMatcherProbe("cancel creation")
    page = show_page(driver)
    page.on_cancel_creation(lambda: cancel_creation_signal.received())

    driver.cancel_creation("Honeycomb", "~Documents", using_shortcut=using_shortcut)
    driver.check(cancel_creation_signal)


def test_selects_an_project_location(driver):
    show_page(driver, select_project_location=lambda handler: handler("/path/to/project"))

    driver.select_project()
    driver.has_location("/path/to/project")


def test_selects_reference_track_location(driver):
    show_page(driver, select_track=lambda type_, handler: handler("track." + type_))

    driver.select_track()
    driver.has_reference_track("track.mp3")


def test_disables_create_button_when_project_name_or_location_missing(driver):
    show_page(driver)

    driver.enter_name("")
    driver.creation_is_disabled()
    driver.enter_name("Honeycomb")
    driver.enter_location("")
    driver.creation_is_disabled()


def test_resets_form_on_show(driver):
    page = show_page(driver)

    driver.enter_name("Honeycomb")
    driver.enter_location("~Documents")
    driver.enter_reference_track("~Music/track.mp3")

    page.hide()
    page.show()

    driver.has_reset_form()


def test_asks_for_confirmation_when_project_file_already_exists(driver):
    project_exists_query = ValueMatcherProbe("check project exists", ("Honeycomb", "~Documents"))
    show_page(driver, project_exists=lambda *args: project_exists_query.received(args))

    driver.create_project("Honeycomb", "~Documents")
    driver.check(project_exists_query)


def test_creates_project_if_confirmed(driver):
    create_project_signal = ValueMatcherProbe("new project", ("flac", "Honeycomb", "~Documents", "track.flac"))
    show_page(driver, of_type="flac", project_exists=yes, on_create_project=lambda *args: create_project_signal.received(args))

    driver.create_project("Honeycomb", "~Documents", "track.flac")
    driver.check(create_project_signal)
