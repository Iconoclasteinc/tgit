# -*- coding: utf-8 -*-

from test.integration.ui.base_widget_test import BaseWidgetTest
from test.cute.probes import ValueMatcherProbe
from test.cute.finders import WidgetIdentity
from test.drivers.welcome_screen_driver import WelcomeScreenDriver

from tgit.ui.welcome_screen import WelcomeScreen


class WelcomeScreenTest(BaseWidgetTest):
    def setUp(self):
        super(WelcomeScreenTest, self).setUp()
        self.welcomeScreen = WelcomeScreen()
        self.view(self.welcomeScreen)
        self.tagger = self.createDriverFor(self.welcomeScreen)

    def createDriverFor(self, widget):
        return WelcomeScreenDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testSignalsNewAlbumRequestWhenNewAlbumButtonClicked(self):
        newAlbumRequestMade = ValueMatcherProbe('new album request')

        class NewAlbumListener(object):
            def newAlbum(self):
                newAlbumRequestMade.setReceivedValue(True)

        self.welcomeScreen.addRequestListener(NewAlbumListener())

        self.tagger.newAlbum()
        self.tagger.check(newAlbumRequestMade)
