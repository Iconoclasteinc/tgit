import pytest

from cute.matchers import named
from cute.widgets import window
from test.ui import ignore, no, show_, close_
from testing.drivers import StartupScreenDriver
from tgit.ui.pages.new_project_page import NewProjectPage
from tgit.ui.pages.startup_screen import StartupScreen
from tgit.ui.pages.welcome_page import WelcomePage

pytestmark = pytest.mark.ui


def show_screen():
    def create_welcome_page():
        return WelcomePage(select_project=ignore, show_load_error=ignore)

    def create_new_project_page():
        return NewProjectPage(select_location=ignore, select_track=ignore, check_project_exists=no,
                              confirm_overwrite=ignore)

    startup_screen = StartupScreen(create_welcome_page=create_welcome_page,
                                   create_new_project_page=create_new_project_page)
    show_(startup_screen)
    return startup_screen


@pytest.yield_fixture()
def driver(prober, automaton):
    screen_driver = StartupScreenDriver(window(StartupScreen, named("startup_screen")), prober, automaton)
    yield screen_driver
    close_(screen_driver)


def test_initially_shows_the_welcome_page(driver):
    _ = show_screen()
    driver.shows_welcome_page()


def test_opens_new_project_page_to_create_a_project(driver):
    _ = show_screen()
    driver.create_project()


def test_returns_to_welcome_page_after_cancelling_project_creation(driver):
    _ = show_screen()
    driver.cancel_creation()
