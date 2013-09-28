# -*- coding: utf-8 -*-

import unittest
from flexmock import flexmock
from tests.integration.ui.base_widget_test import BaseWidgetTest

from tests.cute.finders import WidgetIdentity
from tests.drivers.album_panel_driver import AlbumPanelDriver
from tests.util import resources, fs
from tgit.ui.album_panel import AlbumPanel
# todo consider moving all ui constants to the same module (ui?)
from tgit.ui import album_panel as ui


def buildTrack(**tags):
    defaults = dict(releaseName=None,
                    frontCoverPicture=(None, None),
                    leadPerformer=None,
                    releaseDate=None,
                    upc=None)
    return flexmock(**dict(defaults.items() + tags.items()))


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
        track = buildTrack(frontCoverPicture=frontCover)
        self.albumPanel.trackSelected(track)
        self.driver.displaysFrontCoverPictureWithSize(*ui.FRONT_COVER_DISPLAY_SIZE)

    @unittest.skip("todo")
    def testLetsUserSelectAFrontCoverPicture(self):
        raise AssertionError("Not yet implemented")

    def testDisplaysReleaseName(self):
        track = buildTrack(releaseName='Release Name')
        self.albumPanel.trackSelected(track)
        self.driver.showsReleaseName('Release Name')

    def testDisplaysLeadPerformer(self):
        track = buildTrack(leadPerformer='Lead Performer')
        self.albumPanel.trackSelected(track)
        self.driver.showsLeadPerformer('Lead Performer')

    def testDisplaysReleaseDate(self):
        track = buildTrack(releaseDate='2009-08-05')
        self.albumPanel.trackSelected(track)
        self.driver.showsReleaseDate('2009-08-05')

    def testDisplaysSelectedTrackAlbumUpc(self):
        track = buildTrack(upc='1234567899999')
        self.albumPanel.trackSelected(track)
        self.driver.showsUpc('1234567899999')
