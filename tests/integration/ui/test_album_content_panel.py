# -*- coding: utf-8 -*-

from datetime import timedelta
from flexmock import flexmock
from tests.integration.ui.base_widget_test import BaseWidgetTest

from tests.cute.finders import WidgetIdentity
from tests.drivers.album_content_panel_driver import AlbumContentPanelDriver
from tgit.ui.album_content_panel import AlbumContentPanel


# todo extract that to a builders module
def buildTrack(**tags):
    defaults = dict(trackTitle=None,
                    duration=timedelta(minutes=3, seconds=30).total_seconds())
    return flexmock(**dict(defaults.items() + tags.items()))


class AlbumContentPanelTest(BaseWidgetTest):
    def setUp(self):
        super(AlbumContentPanelTest, self).setUp()
        self.panel = AlbumContentPanel()
        self.view(self.panel)
        self.driver = self.createDriverFor(self.panel)

    def createDriverFor(self, widget):
        return AlbumContentPanelDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysColumnHeadings(self):
        self.driver.showsColumnHeadings('Track Title', 'Duration')

    def testDisplaysTrackTitle(self):
        track = buildTrack(trackTitle='Banana Song')
        self.panel.setTrack(track)
        self.driver.showsTrackTitle('Banana Song')

    def testDisplaysTrackDuration(self):
        track = buildTrack(duration=timedelta(minutes=3, seconds=43).total_seconds())
        self.panel.setTrack(track)
        self.driver.showsTrackDuration('03:43')
