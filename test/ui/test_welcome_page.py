import pytest
from hamcrest import instance_of, starts_with

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers import WelcomePageDriver
from test.ui import ignore, show_, close_
from test.util.builders import make_project_history, make_snapshot
from tgit.ui.pages.welcome_page import make_welcome_page, WelcomePage

pytestmark = pytest.mark.ui


def show_page(project_history=make_project_history(), select_project=ignore, show_load_error=ignore, **handlers):
    page = make_welcome_page(project_history, select_project, show_load_error, **handlers)
    show_(page)
    return page


@pytest.yield_fixture()
def driver(prober, automaton):
    page_driver = WelcomePageDriver(window(WelcomePage, named("welcome_page")), prober, automaton)
    yield page_driver
    close_(page_driver)


def test_signals_project_creation_with_project_type_when_new_project_button_clicked(driver):
    new_project_signal = ValueMatcherProbe("new project", "mp3")
    _ = show_page(on_create_project=new_project_signal.received)

    driver.new_project()
    driver.check(new_project_signal)


def test_signals_project_load_when_load_project_button_clicked(driver):
    load_project_signal = ValueMatcherProbe("load project", "project.tgit")
    _ = show_page(select_project=lambda on_select: on_select("project.tgit"),
                  on_load_project=load_project_signal.received)

    driver.load()
    driver.check(load_project_signal)


def test_warns_user_when_project_load_fails(driver):
    def load_fails(_):
        raise OSError("Load failed")

    load_failed_signal = ValueMatcherProbe("load project failed", instance_of(OSError))

    _ = show_page(select_project=lambda load: load("project.tgit"),
                  show_load_error=load_failed_signal.received,
                  on_load_project=load_fails)

    driver.load()
    driver.check(load_failed_signal)


def test_displays_project_history(driver):
    _ = show_page(make_project_history(make_snapshot(name="Last", type_="mp3", path="last.tgit"),
                                       make_snapshot(name="Previous", type_="flac", path="previous.tgit"),
                                       make_snapshot(name="Oldest", type_="mp3", path="oldest.tgit")))

    driver.shows_recent_projects("Last (mp3)", "Previous (flac)", "Oldest (mp3)")


def test_clears_previous_history_on_display(driver):
    page = show_page(make_project_history(make_snapshot(name="1", path="previous.tgit"),
                                          make_snapshot(name="2", path="oldest.tgit")))

    page.display_project_history(make_project_history(make_snapshot(name="1", path="last.tgit")))
    driver.shows_recent_projects(starts_with("1"))


@pytest.mark.parametrize("using", ["double-click", "button", "enter"])
def test_signals_project_to_open_when_open_action_triggered(driver, using):
    signal = ValueMatcherProbe("open project", "project.tgit")

    _ = show_page(make_project_history(make_snapshot(name="project", path="project.tgit")),
                  on_load_project=signal.received)

    driver.open_recent_project(starts_with("project"), using=using)
    driver.check(signal)


def test_disables_open_project_when_no_project_selected(driver):
    _ = show_page(make_project_history(make_snapshot(name="project")))

    driver.has_disabled_open_project()
    driver.select_project(starts_with("project"))
    driver.has_enabled_open_project()
