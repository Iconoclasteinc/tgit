# -*- coding: utf-8 -*-

from test.integration.ui import ViewTest
from test.cute.probes import ValueMatcherProbe
from test.cute.finders import WidgetIdentity
from test.drivers.welcome_screen_driver import WelcomeScreenDriver

from tgit.ui.welcome_screen import WelcomeScreen


class WelcomeScreenTest(ViewTest):
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
        self.driver.newAlbum()
        self.driver.check(newAlbumSignal)