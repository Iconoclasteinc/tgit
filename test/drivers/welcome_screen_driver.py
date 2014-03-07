# -*- coding: utf-8 -*-

from PyQt4.QtGui import QPushButton, QWidget

from test.cute.matchers import named
from test.cute.widgets import WidgetDriver, ButtonDriver
from tgit.ui.welcome_screen import WelcomeScreen


def welcomeScreen(parent):
    return WelcomeScreenDriver.findSingle(parent, QWidget, named(WelcomeScreen.NAME))


class WelcomeScreenDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(WelcomeScreenDriver, self).__init__(selector, prober, gesturePerformer)

    def newAlbum(self):
        button = ButtonDriver.findSingle(self, QPushButton,
                                         named(WelcomeScreen.NEW_ALBUM_BUTTON_NAME))
        button.click()