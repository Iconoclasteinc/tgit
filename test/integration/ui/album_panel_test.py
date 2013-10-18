# -*- coding: utf-8 -*-

import unittest
from hamcrest import equal_to, contains, has_length, has_properties

from test.integration.ui.base_widget_test import BaseWidgetTest
from test.cute.probes import AssertionProbe
from test.cute.finders import WidgetIdentity
from test.drivers.album_panel_driver import AlbumPanelDriver
from test.util import resources, fs, builders

from tgit.metadata import Image
from tgit.album import Album
# todo consider moving all ui constants to the same module (ui?)
from tgit.ui import album_panel as ui
from tgit.ui.album_panel import AlbumPanel


def loadImage(name):
    return fs.readContent(resources.path(name))


class AlbumPanelTest(BaseWidgetTest):
    def setUp(self):
        super(AlbumPanelTest, self).setUp()
        self.album = Album()
        self.albumPanel = AlbumPanel(self.album)
        self.view(self.albumPanel)
        self.tagger = self.createDriverFor(self.albumPanel)

    def createDriverFor(self, widget):
        return AlbumPanelDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysFrontCoverScaledToPictureDisplayArea(self):
        self.albumPanel.albumStateChanged(builders.album(
            images=[builders.image('image/jpeg', loadImage('front-cover.jpg'))]
        ))
        self.tagger.displaysFrontCoverPictureWithSize(*ui.FRONT_COVER_DISPLAY_SIZE)

    @unittest.skip("todo")
    def testLetsUserSelectAFrontCoverPicture(self):
        # probe that we use a picture selector
        raise NotImplementedError()

    def testDisplaysAlbumMetadata(self):
        self.albumPanel.albumStateChanged(builders.album(
            releaseName='Album',
            leadPerformer='Artist',
            guestPerformers='Band',
            labelName='Label',
            recordingTime='2008-09-15',
            releaseTime='2009-01-01',
            originalReleaseTime='1998-03-05',
            upc='Code'))

        self.tagger.showsReleaseName('Album')
        self.tagger.showsLeadPerformer('Artist')
        self.tagger.showsGuestPerformers('Band')
        self.tagger.showsLabelName('Label')
        self.tagger.showsRecordingTime('2008-09-15')
        self.tagger.showsReleaseTime('2009-01-01')
        self.tagger.showsOriginalReleaseTime('1998-03-05')
        self.tagger.showsUpc('Code')

    def testUpdatesAlbumOnMetadataChange(self):
        self.tagger.changeFrontCoverPicture(resources.path('front-cover.jpg'))
        self.check(AssertionProbe(self.album.images, contains(
            has_properties(
                mime='image/jpeg',
                data=has_length(len(loadImage('front-cover.jpg'))),
                type=Image.FRONT_COVER,
                desc='Front Cover')), 'front cover picture'))

        self.tagger.changeReleaseName('Album')
        self.check(AssertionProbe(self.album.releaseName, equal_to('Album'), 'release name'))

        self.tagger.changeLeadPerformer('Artist')
        self.check(AssertionProbe(self.album.leadPerformer, equal_to('Artist'), 'lead performer'))

        self.tagger.changeGuestPerformers('Band')
        self.check(AssertionProbe(self.album.guestPerformers, equal_to('Band'), 'guest performers'))

        self.tagger.changeLabelName('Label')
        self.check(AssertionProbe(self.album.labelName, equal_to('Label'), 'label name'))

        self.tagger.changeRecordingTime('2008-09-15')
        self.check(AssertionProbe(self.album.recordingTime, equal_to('2008-09-15'),
                                  'recording time'))

        self.tagger.changeReleaseTime('2009-01-01')
        self.check(AssertionProbe(self.album.releaseTime, equal_to('2009-01-01'), 'release time'))

        self.tagger.changeOriginalReleaseTime('1998-03-05')
        self.check(AssertionProbe(self.album.originalReleaseTime, equal_to('1998-03-05'),
                                  'original release time'))

        self.tagger.changeUpc('Barcode')
        self.check(AssertionProbe(self.album.upc, equal_to('Barcode'), 'upc'))