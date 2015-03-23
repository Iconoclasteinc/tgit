# -*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget

from test.cute4.matchers import named
from test.drivers4.__base import BaseDriver


def welcomeScreen(parent):
    return WelcomeScreenDriver.findSingle(parent, QWidget, named('welcome-screen'))


class WelcomeScreenDriver(BaseDriver):
    def newAlbum(self):
        self.button(named('new-album')).click()