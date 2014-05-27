# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences

from test.integration.ui.views import ViewTest
from test.cute.probes import ValueMatcherProbe
from test.cute.finders import WidgetIdentity
from test.drivers.welcome_screen_driver import WelcomeScreenDriver

from tgit.ui.views.welcome_screen import WelcomeScreen


class WelcomeScreenTest(ViewTest):
    def setUp(self):
        super(WelcomeScreenTest, self).setUp()
        self.view = WelcomeScreen()
        self.show(self.view)
        self.driver = self.createDriverFor(self.view)

    def createDriverFor(self, widget):
        return WelcomeScreenDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testSignalsWhenNewAlbumButtonClicked(self):
        newAlbumSignal = ValueMatcherProbe('new album')
        self.view.bind(newAlbum=newAlbumSignal.received)
        self.driver.newAlbum()
        self.driver.check(newAlbumSignal)