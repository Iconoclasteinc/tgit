# -*- coding: utf-8 -*-

from cute.matchers import named
from test.drivers._screen_driver import ScreenDriver
from tgit.ui.welcome_screen import WelcomeScreen


def welcome_screen(parent):
    return WelcomeScreenDriver.find_single(parent, WelcomeScreen, named("welcome_screen"))


class WelcomeScreenDriver(ScreenDriver):
    def import_album(self):
        self.button(named("import_album_button")).click()

    def new_album(self, of_type):
        self.button(named("new_{0}_album_button".format(of_type))).click()
