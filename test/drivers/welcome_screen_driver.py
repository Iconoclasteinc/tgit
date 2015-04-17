# -*- coding: utf-8 -*-

from test.cute.matchers import named
from test.drivers import BaseDriver
from tgit.ui.welcome_screen import WelcomeScreen


def welcomeScreen(parent):
    return WelcomeScreenDriver.findSingle(parent, WelcomeScreen, named('welcome-screen'))


class WelcomeScreenDriver(BaseDriver):
    def newAlbum(self):
        self.button(named('new-album')).click()