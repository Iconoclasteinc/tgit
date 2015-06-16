# -*- coding: utf-8 -*-

from cute.matchers import named
from tgit.ui.welcome_page import WelcomePage
from ._screen_driver import ScreenDriver


def welcome_page(parent):
    return WelcomePageDriver.find_single(parent, WelcomePage, named("welcome_page"))


class WelcomePageDriver(ScreenDriver):
    def new_album(self, of_type):
        self.button(named("new_{0}_album_button".format(of_type))).click()

    def load(self):
        self.button(named("load_album_button")).click()
