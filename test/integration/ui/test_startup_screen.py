import pytest

from cute.finders import WidgetIdentity
from cute.matchers import named
from cute.widgets import window
from test.drivers.startup_screen_driver import StartupScreenDriver
from test.integration.ui import show_widget
from tgit.ui.pages.new_project_page import NewProjectPage
from tgit.ui.pages.startup_screen import StartupScreen
from tgit.ui.pages.welcome_page import WelcomePage

pytestmark = pytest.mark.ui

ignore = lambda: None
no = lambda _: False


def show_screen(page_driver):
    def create_welcome_page():
        return WelcomePage(select_project=ignore, show_load_error=ignore)

    def create_new_project_page():
        return NewProjectPage(select_location=ignore, select_track=ignore, check_project_exists=no,
                              confirm_overwrite=ignore)

    startup_screen = StartupScreen(create_welcome_page=create_welcome_page,
                                   create_new_project_page=create_new_project_page)
    show_widget(page_driver, startup_screen)
    return startup_screen


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    wizard_driver = StartupScreenDriver(window(StartupScreen, named("startup_screen")), prober, automaton)
    yield wizard_driver
    wizard_driver.close()


def test_initially_shows_the_welcome_page(driver):
    show_screen(driver)
    driver.shows_welcome_page()


def test_opens_new_project_page_to_create_a_project(driver):
    show_screen(driver)
    driver.create_project()


def test_returns_to_welcome_page_after_cancelling_project_creation(driver):
    show_screen(driver)
    driver.cancel_creation()
