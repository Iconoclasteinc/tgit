# -*- coding: utf-8 -*-

from hamcrest import equal_to, contains, has_length, has_properties

from test.integration.ui.base_widget_test import BaseWidgetTest
from test.cute.probes import AssertionProbe
from test.cute.finders import WidgetIdentity
from test.drivers.album_page_driver import AlbumPageDriver
from test.util import resources
from test.util.fakes import FakeFileChooser

from tgit import fs
from tgit.metadata import Image
from tgit.album import Album
from tgit.ui import constants as ui
from tgit.ui.album_page import AlbumPage


def loadImage(name):
    return fs.readContent(resources.path(name))


class AlbumPageTest(BaseWidgetTest):

    def setUp(self):
        super(AlbumPageTest, self).setUp()
        self.album = Album()
        self.pictureChooser = FakeFileChooser()
        self.widget = AlbumPage(self.album, self.pictureChooser)
        self.view(self.widget)
        self.driver = self.createDriverFor(self.widget)

    def createDriverFor(self, widget):
        return AlbumPageDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysFrontCoverScaledToPictureDisplayArea(self):
        self.album.addImage('image/jpeg', loadImage('front-cover.jpg'))
        self.driver.displaysFrontCoverPictureWithSize(*ui.FRONT_COVER_PIXMAP_SIZE)

    def testDisplaysAlbumMetadata(self):
        self.album.releaseName = 'Album'
        self.driver.showsReleaseName('Album')
        self.album.leadPerformer = 'Artist'
        self.driver.showsLeadPerformer('Artist')
        self.album.guestPerformers = [('Guitar', 'Guitarist'), ('Piano', 'Pianist')]
        self.driver.showsGuestPerformers('Guitar: Guitarist; Piano: Pianist')
        self.album.labelName = 'Label'
        self.driver.showsLabelName('Label')
        self.album.catalogNumber = 'Number'
        self.driver.showsCatalogNumber('Number')
        self.album.upc = 'Code'
        self.driver.showsUpc('Code')
        self.album.recordingTime = '2008-09-15'
        self.driver.showsRecordingTime('2008-09-15')
        self.album.releaseTime = '2009-01-01'
        self.driver.showsReleaseTime('2009-01-01')
        self.album.originalReleaseTime = '1998-03-05'
        self.driver.showsOriginalReleaseTime('1998-03-05')
        self.album.recordingStudios = 'Studio A, Studio B'
        self.driver.showsRecordingStudios('Studio A, Studio B')
        self.album.producer = 'Artistic Producer'
        self.driver.showsProducer('Artistic Producer')
        self.album.mixer = 'Mixing Engineer'
        self.driver.showsMixer('Mixing Engineer')

    def testUpdatesAlbumWhenMetadataEdited(self):
        self.pictureChooser.chooses(resources.path('front-cover.jpg'))
        self.driver.selectFrontCover()
        self.check(AssertionProbe(self.album.images, contains(
            has_properties(
                mime='image/jpeg',
                data=has_length(len(loadImage('front-cover.jpg'))),
                type=Image.FRONT_COVER,
                desc='Front Cover')), 'front cover picture'))

        self.driver.changeReleaseName('Album')
        self.check(AssertionProbe(self.album.releaseName, equal_to('Album'), 'release name'))

        self.driver.changeLeadPerformer('Artist')
        self.check(AssertionProbe(self.album.leadPerformer, equal_to('Artist'), 'lead performer'))

        self.driver.changeGuestPerformers('Guitar: Guitarist; Guitar: Bassist; Piano: Pianist')
        self.check(AssertionProbe(self.album.guestPerformers, equal_to(
            [('Guitar', 'Guitarist'), ('Guitar', 'Bassist'), ('Piano', 'Pianist')]),
            'guest performers'))

        self.driver.changeLabelName('Label')
        self.check(AssertionProbe(self.album.labelName, equal_to('Label'), 'label name'))

        self.driver.changeCatalogNumber('Number')
        self.check(AssertionProbe(self.album.catalogNumber, equal_to('Number'), 'catalog number'))

        self.driver.changeUpc('Barcode')
        self.check(AssertionProbe(self.album.upc, equal_to('Barcode'), 'upc'))

        self.driver.changeRecordingTime('2008-09-15')
        self.check(AssertionProbe(self.album.recordingTime, equal_to('2008-09-15'),
                                  'recording time'))

        self.driver.changeReleaseTime('2009-01-01')
        self.check(AssertionProbe(self.album.releaseTime, equal_to('2009-01-01'), 'release time'))

        self.driver.changeOriginalReleaseTime('1998-03-05')
        self.check(AssertionProbe(self.album.originalReleaseTime, equal_to('1998-03-05'),
                                  'original release time'))

        self.driver.changeRecordingStudios('Studios')
        self.check(AssertionProbe(self.album.recordingStudios, equal_to('Studios'),
                                  'recording studios'))

        self.driver.changeProducer('Producer')
        self.check(AssertionProbe(self.album.producer, equal_to('Producer'), 'producer'))

        self.driver.changeMixer('Mixing Engineer')
        self.check(AssertionProbe(self.album.mixer, equal_to('Mixing Engineer'), 'mixer'))