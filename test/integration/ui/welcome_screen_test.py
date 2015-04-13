# -*- coding: utf-8 -*-

from test.cute.probes import ValueMatcherProbe
from test.cute.finders import WidgetIdentity
from test.drivers.welcome_screen_driver import WelcomeScreenDriver
from test.integration.ui import WidgetTest

from tgit.ui.welcome_screen import WelcomeScreen


class WelcomeScreenTest(WidgetTest):
    def setUp(self):
        super().setUp()
        self.screen = WelcomeScreen()
        self.show(self.screen)
        self.driver = self.create_driver_for(self.screen)

    def create_driver_for(self, widget):
        return WelcomeScreenDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testSignalsWhenNewAlbumButtonClicked(self):
        new_album_signal = ValueMatcherProbe('new album')
        self.screen.create_new_album.connect(new_album_signal.received)
        self.driver.newAlbum()
        self.driver.check(new_album_signal)