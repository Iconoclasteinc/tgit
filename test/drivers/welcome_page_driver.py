from PyQt5.QtWidgets import QListView, QAbstractButton

from cute import matchers as match
from cute.matchers import named
from cute.widgets import QListViewDriver, ButtonDriver
from tgit.ui.pages.welcome_page import WelcomePage
from ._screen_driver import ScreenDriver


def welcome_page(parent):
    return WelcomePageDriver.find_single(parent, WelcomePage, named("welcome_page"))


class WelcomePageDriver(ScreenDriver):
    def __init__(self, selector, prober, gesture_performer):
        super().__init__(selector, prober, gesture_performer)

    def new_project(self, of_type="mp3"):
        self.button(named("_new_{}_project_button".format(of_type))).click()

    def load(self):
        self._load_project_button.click()

    def select_project(self, path):
        self._recent_projects_list.select_item(match.with_item_text(path))

    def has_disabled_open_project(self):
        self._open_project_button.is_disabled()

    def has_enabled_open_project(self):
        self._open_project_button.is_enabled()

    def shows_recent_projects(self, *entries):
        self._recent_projects_list.contains_items(*[match.with_item_text(entry) for entry in entries])

    def open_recent_project(self, name):
        self.select_project(name)
        self._open_project_button.click()

    @property
    def _recent_projects_list(self):
        return QListViewDriver.find_single(self, QListView, named("_recent_projects_list"))

    @property
    def _open_project_button(self):
        return ButtonDriver.find_single(self, QAbstractButton, named("_open_project_button"))

    @property
    def _load_project_button(self):
        return self.button(named("_load_project_button"))
