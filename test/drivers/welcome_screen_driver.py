# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget

from test.cute.matchers import named
from test.drivers import BaseDriver


def welcomeScreen(parent):
    return WelcomeScreenDriver.findSingle(parent, QWidget, named('welcome_screen'))


class WelcomeScreenDriver(BaseDriver):
    def newAlbum(self):
        self.button(named('new_album')).click()