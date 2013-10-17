# -*- coding: utf-8 -*-

import unittest
from hamcrest import assert_that, equal_to, contains, has_length

from test.integration.ui.base_widget_test import BaseWidgetTest
from test.cute.finders import WidgetIdentity
from test.drivers.album_panel_driver import AlbumPanelDriver
from test.util import resources, fs, doubles

from tgit.album import Album
from tgit.track import Track
# todo consider moving all ui constants to the same module (ui?)
from tgit.ui import album_panel as ui
from tgit.ui.album_panel import AlbumPanel


def loadImage(name):
    return fs.readContent(resources.path(name))


class AlbumPanelTest(BaseWidgetTest):
    def setUp(self):
        super(AlbumPanelTest, self).setUp()
        self.album = Album()
        self.album.appendTrack(Track(doubles.audio()))
        self.albumPanel = AlbumPanel(self.album)
        self.view(self.albumPanel)
        self.tagger = self.createDriverFor(self.albumPanel)

    def createDriverFor(self, widget):
        return AlbumPanelDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysFrontCoverScaledToPictureDisplayArea(self):
        self.album.frontCoverPicture = 'image/jpeg', loadImage("front-cover"".jpg")
        self.albumPanel.albumStateChanged(self.album)
        self.tagger.displaysFrontCoverPictureWithSize(*ui.FRONT_COVER_DISPLAY_SIZE)

    @unittest.skip("todo")
    def testLetsUserSelectAFrontCoverPicture(self):
        # probe that we use a picture selector
        raise AssertionError("Not yet implemented")

    def testDisplaysAlbumMetadata(self):
        self.album.releaseName = 'Album'
        self.album.leadPerformer = 'Artist'
        self.album.guestPerformers = 'Band'
        self.album.labelName = 'Label'
        self.album.recordingTime = '2008-09-15'
        self.album.releaseTime = '2009-01-01'
        self.album.originalReleaseTime = '1998-03-05'
        self.album.upc = 'Code'

        self.albumPanel.albumStateChanged(self.album)
        self.tagger.showsReleaseName('Album')
        self.tagger.showsLeadPerformer('Artist')
        self.tagger.showsGuestPerformers('Band')
        self.tagger.showsLabelName('Label')
        self.tagger.showsRecordingTime('2008-09-15')
        self.tagger.showsReleaseTime('2009-01-01')
        self.tagger.showsOriginalReleaseTime('1998-03-05')
        self.tagger.showsUpc('Code')

    def testUpdatesAlbumMetadataWithUserEntries(self):
        picture = resources.path("front-cover.jpg")
        self.tagger.changeFrontCoverPicture(picture)
        self.tagger.changeReleaseName('Album')
        self.tagger.changeLeadPerformer('Artist')
        self.tagger.changeGuestPerformers('Band')
        self.tagger.changeLabelName('Label')
        self.tagger.changeRecordingTime('2008-09-15')
        self.tagger.changeReleaseTime('2009-01-01')
        self.tagger.changeOriginalReleaseTime('1998-03-05')
        self.tagger.changeUpc('Barcode')

        self.albumPanel.updateAlbum()
        mime, data = fs.guessMimeType(picture), fs.readContent(picture)
        assert_that(self.album.frontCoverPicture, contains(mime, has_length(len(data))),
                    'front cover picture')
        assert_that(self.album.releaseName, equal_to('Album'), 'release name')
        assert_that(self.album.leadPerformer, equal_to('Artist'), 'lead performer')
        assert_that(self.album.guestPerformers, equal_to('Band'), 'guest performers')
        assert_that(self.album.labelName, equal_to('Label'), 'label name')
        assert_that(self.album.recordingTime, equal_to('2008-09-15'), 'recording time')
        assert_that(self.album.releaseTime, equal_to('2009-01-01'), 'release time')
        assert_that(self.album.originalReleaseTime, equal_to('1998-03-05'),
                    'original release time')
        assert_that(self.album.upc, equal_to('Barcode'), 'upc')
