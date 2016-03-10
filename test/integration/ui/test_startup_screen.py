import pytest

from cute.finders import WidgetIdentity
from test.drivers.startup_screen_driver import StartupScreenDriver
from test.integration.ui import show_widget
from tgit.ui.pages.new_project_page import NewProjectPage
from tgit.ui.pages.startup_screen import StartupScreen
from tgit.ui.pages.welcome_page import WelcomePage

pytestmark = pytest.mark.ui

ignore = lambda: None
no = lambda _: False


@pytest.fixture()
def screen(qt):
    def create_welcome_page():
        return WelcomePage(select_project=ignore, show_load_error=ignore)

    def create_new_project_page():
        return NewProjectPage(select_location=ignore, select_track=ignore, check_project_exists=no,
                              confirm_overwrite=ignore)

    startup_screen = StartupScreen(create_welcome_page=create_welcome_page,
                                   create_new_project_page=create_new_project_page)
    show_widget(startup_screen)
    return startup_screen


@pytest.yield_fixture()
def driver(screen, prober, automaton):
    wizard_driver = StartupScreenDriver(WidgetIdentity(screen), prober, automaton)
    yield wizard_driver
    wizard_driver.close()


def test_initially_shows_the_welcome_page(driver):
    driver.shows_welcome_page()


def test_opens_new_project_page_to_create_a_project(driver):
    driver.create_project()


def test_returns_to_welcome_page_after_cancelling_project_creation(driver):
    driver.cancel_creation()
