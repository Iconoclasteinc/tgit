# -*- coding: utf-8 -*-

from cute.matchers import named
from tgit.ui.pages.welcome_page import WelcomePage
from ._screen_driver import ScreenDriver


def welcome_page(parent):
    return WelcomePageDriver.find_single(parent, WelcomePage, named("welcome_page"))


class WelcomePageDriver(ScreenDriver):
    def new_project(self):
        self.button(named("_new_mp3_project_button")).click()

    def load(self):
        self.button(named("_load_project_button")).click()
