import pytest
from hamcrest import instance_of

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers import WelcomePageDriver
from test.ui import ignore, show_, close_
from test.util.builders import make_project_history
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
    _ = show_page(make_project_history("/path/to/oldest/project", "/path/to/previous/project", "/path/to/last/project"))

    driver.shows_recent_projects("/path/to/last/project", "/path/to/previous/project", "/path/to/oldest/project")


def test_clears_previous_history_on_display(driver):
    page = show_page(make_project_history("/path/to/oldest/project", "/path/to/previous/project"))

    page.display_project_history(make_project_history("/path/to/last/project"))
    driver.shows_recent_projects("/path/to/last/project")


def test_signals_project_to_open_when_open_button_clicked(driver):
    signal = ValueMatcherProbe("open project", "/path/to/project/file")

    _ = show_page(make_project_history("/path/to/project/file"), on_load_project=signal.received)

    driver.open_recent_project("/path/to/project/file")
    driver.check(signal)


def test_disables_open_project_when_no_project_selected(driver):
    _ = show_page(make_project_history("/path/to/project/file"))

    driver.has_disabled_open_project()
    driver.select_project("/path/to/project/file")
    driver.has_enabled_open_project()

