from hamcrest import instance_of
import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers import WelcomePageDriver
from test.integration.ui import ignore
from tgit.ui.pages.welcome_page import WelcomePage, make_welcome_page

pytestmark = pytest.mark.ui


def show_page(page_driver, select_project=ignore, show_load_error=ignore, **handlers):
    page = make_welcome_page(select_project, show_load_error, **handlers)
    page_driver.show()
    return page


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    page_driver = WelcomePageDriver(window(WelcomePage, named("welcome_page")), prober, automaton)
    yield page_driver
    page_driver.close()


def test_signals_when_new_project_button_clicked(driver):
    new_project_signal = ValueMatcherProbe("new project", "mp3")
    _ = show_page(driver, on_create_project=new_project_signal.received)

    driver.new_project()
    driver.check(new_project_signal)


def test_signals_when_load_project_button_clicked(driver):
    load_project_signal = ValueMatcherProbe("load project", "project.tgit")
    _ = show_page(driver,
                  select_project=lambda on_select: on_select("project.tgit"),
                  on_load_project=load_project_signal.received)

    driver.load()
    driver.check(load_project_signal)


def test_warn_user_if_load_failed(driver):
    def load_fails(_):
        raise OSError("Load failed")

    load_failed_signal = ValueMatcherProbe("load project failed", instance_of(OSError))

    _ = show_page(driver,
                  select_project=lambda load: load("project.tgit"),
                  show_load_error=load_failed_signal.received,
                  on_load_project=load_fails)

    driver.load()
    driver.check(load_failed_signal)
