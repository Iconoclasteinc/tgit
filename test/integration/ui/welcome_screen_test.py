# -*- coding: utf-8 -*-

from test.integration.ui.view_test import ViewTest
from test.cute.probes import ValueMatcherProbe
from test.cute.finders import WidgetIdentity
from test.drivers.welcome_screen_driver import WelcomeScreenDriver

from tgit.ui.welcome_screen import WelcomeScreen


class WelcomeScreenTest(ViewTest):
    def setUp(self):
        super(WelcomeScreenTest, self).setUp()
        self.widget = WelcomeScreen()
        self.show(self.widget)
        self.driver = self.createDriverFor(self.widget)

    def createDriverFor(self, widget):
        return WelcomeScreenDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testCreatesNewAlbumWhenNewAlbumButtonClicked(self):
        newAlbumRequest = ValueMatcherProbe('new album')

        class RequestTracker(object):
            def newAlbum(self):
                newAlbumRequest.received()

        self.widget.addRequestListener(RequestTracker())
        self.driver.newAlbum()
        self.driver.check(newAlbumRequest)
