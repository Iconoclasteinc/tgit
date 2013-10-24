# -*- coding: utf-8 -*-

from PyQt4.QtGui import QPushButton

from test.cute.matchers import named
from test.cute.widgets import WidgetDriver, AbstractButtonDriver

from tgit.ui import constants as ui


class WelcomeScreenDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(WelcomeScreenDriver, self).__init__(selector, prober, gesturePerformer)

    def newAlbum(self):
        button = AbstractButtonDriver.findSingle(self, QPushButton, named(ui.NEW_ALBUM_BUTTON_NAME))
        button.click()