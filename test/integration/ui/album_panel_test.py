# -*- coding: utf-8 -*-

import unittest

from test.integration.ui.base_widget_test import BaseWidgetTest
from test.cute.finders import WidgetIdentity
from test.drivers.album_panel_driver import AlbumPanelDriver
from test.util import resources, fs, doubles

# todo consider moving all ui constants to the same module (ui?)
from tgit.ui import album_panel as ui
from tgit.ui.album_panel import AlbumPanel


class AlbumPanelTest(BaseWidgetTest):
    def setUp(self):
        super(AlbumPanelTest, self).setUp()
        self.albumPanel = AlbumPanel()
        self.view(self.albumPanel)
        self.tagger = self.createDriverFor(self.albumPanel)

    def createDriverFor(self, widget):
        return AlbumPanelDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    @unittest.skip("todo")
    def testHasNothingToShowWhenAlbumHasNoMetadata(self):
        raise AssertionError("Not yet implemented")

    def testDisplaysFrontCoverScaledToPictureDisplayArea(self):
        frontCover = ('image/jpeg', fs.readContent(resources.path("front-cover.jpg")))
        track = doubles.track(frontCoverPicture=frontCover)
        self.albumPanel.setTrack(track)
        self.tagger.displaysFrontCoverPictureWithSize(*ui.FRONT_COVER_DISPLAY_SIZE)

    @unittest.skip("todo")
    def testLetsUserSelectAFrontCoverPicture(self):
        # probe that we use a picture selector
        raise AssertionError("Not yet implemented")

    def testDisplaysReleaseName(self):
        track = doubles.track(releaseName='Release Name')
        self.albumPanel.setTrack(track)
        self.tagger.showsReleaseName('Release Name')

    def testDisplaysLeadPerformer(self):
        track = doubles.track(leadPerformer='Lead Performer')
        self.albumPanel.setTrack(track)
        self.tagger.showsLeadPerformer('Lead Performer')

    def testDisplaysGuestPerformers(self):
        track = doubles.track(guestPerformers='Guest Performers')
        self.albumPanel.setTrack(track)
        self.tagger.showsGuestPerformers('Guest Performers')

    def testDisplaysLabelName(self):
        track = doubles.track(labelName='Label Name')
        self.albumPanel.setTrack(track)
        self.tagger.showsLabelName('Label Name')

    def testDisplaysRecordingTime(self):
        track = doubles.track(recordingTime='2009-05-04')
        self.albumPanel.setTrack(track)
        self.tagger.showsRecordingTime('2009-05-04')

    def testDisplaysReleaseTime(self):
        track = doubles.track(releaseTime='2009-08-05')
        self.albumPanel.setTrack(track)
        self.tagger.showsReleaseTime('2009-08-05')

    def testDisplaysOriginalReleaseTime(self):
        track = doubles.track(originalReleaseTime='1980-02-29')
        self.albumPanel.setTrack(track)
        self.tagger.showsOriginalReleaseTime('1980-02-29')

    def testDisplaysUpc(self):
        track = doubles.track(upc='1234567899999')
        self.albumPanel.setTrack(track)
        self.tagger.showsUpc('1234567899999')