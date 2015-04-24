# -*- coding: utf-8 -*-

from cute.matchers import named
from test.drivers import BaseDriver
from tgit.ui.welcome_screen import WelcomeScreen


def welcome_screen(parent):
    return WelcomeScreenDriver.findSingle(parent, WelcomeScreen, named('welcome-screen'))


class WelcomeScreenDriver(BaseDriver):
    def new_album(self):
        self.button(named('new-album')).click()