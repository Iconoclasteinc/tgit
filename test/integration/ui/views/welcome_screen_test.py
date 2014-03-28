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
        self.widget = self.view.render()
        self.show(self.widget)
        self.driver = self.createDriverFor(self.widget)

    def createDriverFor(self, widget):
        return WelcomeScreenDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testSignalsWhenNewAlbumButtonClicked(self):
        newAlbumRequest = ValueMatcherProbe('new album')

        class RequestTracker(object):
            def newAlbum(self):
                newAlbumRequest.received()

        self.view.announceTo(RequestTracker())
        self.driver.newAlbum()
        self.driver.check(newAlbumRequest)