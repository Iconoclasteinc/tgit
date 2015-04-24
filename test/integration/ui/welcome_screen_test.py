# -*- coding: utf-8 -*-

from cute.probes import ValueMatcherProbe
from cute.finders import WidgetIdentity
from test.drivers.welcome_screen_driver import WelcomeScreenDriver
from test.integration.ui import WidgetTest

from tgit.ui.welcome_screen import WelcomeScreen


class WelcomeScreenTest(WidgetTest):
    def setUp(self):
        super(WelcomeScreenTest, self).setUp()
        self.screen = WelcomeScreen()
        self.show(self.screen)
        self.driver = self.createDriverFor(self.screen)

    def createDriverFor(self, widget):
        return WelcomeScreenDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testSignalsWhenNewAlbumButtonClicked(self):
        newAlbumSignal = ValueMatcherProbe('new album')
        self.screen.newAlbum.connect(newAlbumSignal.received)
        self.driver.new_album()
        self.driver.check(newAlbumSignal)