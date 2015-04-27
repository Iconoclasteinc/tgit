# -*- coding: utf-8 -*-

from cute.matchers import named
from test.drivers import ScreenDriver
from tgit.ui.welcome_screen import WelcomeScreen


def welcome_screen(parent):
    return WelcomeScreenDriver.find_single(parent, WelcomeScreen, named('welcome-screen'))


class WelcomeScreenDriver(ScreenDriver):
    def new_album(self):
        self.button(named('new-album')).click()