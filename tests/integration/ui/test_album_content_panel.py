# -*- coding: utf-8 -*-

from flexmock import flexmock
from tests.integration.ui.base_widget_test import BaseWidgetTest

from tests.cute.finders import WidgetIdentity
from tests.drivers.album_content_panel_driver import AlbumContentPanelDriver
from tgit.ui.album_content_panel import AlbumContentPanel


# todo extract that to a builders module
def buildTrack(**tags):
    defaults = dict(releaseName=None,
                    frontCoverPicture=(None, None),
                    leadPerformer=None,
                    releaseDate=None,
                    upc=None,
                    trackTitle=None,
                    versionInfo=None,
                    featuredGuest=None,
                    isrc=None,
                    bitrate=96000,
                    duration=200)
    return flexmock(**dict(defaults.items() + tags.items()))


class AlbumContentPanelTest(BaseWidgetTest):
    def setUp(self):
        super(AlbumContentPanelTest, self).setUp()
        self.panel = AlbumContentPanel()
        self.view(self.panel)
        self.driver = self.createDriverFor(self.panel)

    def createDriverFor(self, widget):
        return AlbumContentPanelDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysTrackTitle(self):
        track = buildTrack(trackTitle='Track Title')
        self.panel.setTrack(track)
        self.driver.showsTrackTitle('Track Title')
