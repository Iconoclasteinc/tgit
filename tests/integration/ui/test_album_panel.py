# -*- coding: utf-8 -*-

import unittest

# todo consider moving all ui constants to the same module (ui?)
from tgit.ui import album_panel as ui
from tgit.ui.album_panel import AlbumPanel

from tests.integration.ui.base_widget_test import BaseWidgetTest
from tests.cute.finders import WidgetIdentity
from tests.drivers.album_panel_driver import AlbumPanelDriver
from tests.util import resources, fs, doubles


class AlbumPanelTest(BaseWidgetTest):
    def setUp(self):
        super(AlbumPanelTest, self).setUp()
        self.albumPanel = AlbumPanel()
        self.view(self.albumPanel)
        self.driver = self.createDriverFor(self.albumPanel)

    def createDriverFor(self, widget):
        return AlbumPanelDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysFrontCoverScaledToPictureDisplayArea(self):
        frontCover = ('image/jpeg', fs.readContent(resources.path("front-cover.jpg")))
        track = doubles.track(frontCoverPicture=frontCover)
        self.albumPanel.setTrack(track)
        self.driver.displaysFrontCoverPictureWithSize(*ui.FRONT_COVER_DISPLAY_SIZE)

    @unittest.skip("todo")
    def testLetsUserSelectAFrontCoverPicture(self):
        raise AssertionError("Not yet implemented")

    def testDisplaysReleaseName(self):
        track = doubles.track(releaseName='Release Name')
        self.albumPanel.setTrack(track)
        self.driver.showsReleaseName('Release Name')

    def testDisplaysLeadPerformer(self):
        track = doubles.track(leadPerformer='Lead Performer')
        self.albumPanel.setTrack(track)
        self.driver.showsLeadPerformer('Lead Performer')

    def testDisplaysReleaseDate(self):
        track = doubles.track(releaseDate='2009-08-05')
        self.albumPanel.setTrack(track)
        self.driver.showsReleaseDate('2009-08-05')

    def testDisplaysSelectedTrackAlbumUpc(self):
        track = doubles.track(upc='1234567899999')
        self.albumPanel.setTrack(track)
        self.driver.showsUpc('1234567899999')