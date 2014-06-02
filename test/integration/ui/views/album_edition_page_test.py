# -*- coding: utf-8 -*-
from hamcrest import has_properties

from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe
from test.drivers import AlbumEditionPageDriver
from test.integration.ui.views import ViewTest
from test.util import resources, builders as build
from tgit.metadata import Image

from tgit.ui.views.album_edition_page import AlbumEditionPage
from tgit.util import fs


# todo Our fake image library would load from the tests resources
def loadImage(name):
    return fs.readContent(resources.path(name))


class PictureSelectorStub(object):
    def __init__(self):
        self.selected = build.image()

    def select(self, handler):
        handler(self.selected)


class AlbumEditionPageTest(ViewTest):
    def setUp(self):
        super(AlbumEditionPageTest, self).setUp()
        self.pictureSelector = PictureSelectorStub()
        self.page = AlbumEditionPage(self.pictureSelector)
        self.driver = self.createDriverFor(self.page)
        self.show(self.page)

    def createDriverFor(self, widget):
        return AlbumEditionPageDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysPicturePlaceholderWhenAlbumHasNoCover(self):
        self.page.display(build.album())
        self.driver.showsPicturePlaceholder()

    def testDisplaysMainAlbumCoverWhenExisting(self):
        self.page.display(build.album(images=[build.image('image/jpeg', loadImage('front-cover.jpg'), Image.FRONT_COVER)]))
        self.driver.showsPicture()

    def testDisplaysAlbumMetadata(self):
        self.page.display(build.album(
            releaseName='Album',
            leadPerformer='Artist',
            guestPerformers=[('Guitar', 'Guitarist'), ('Piano', 'Pianist')],
            labelName='Label',
            catalogNumber='XXX123456789',
            upc='123456789999',
            recordingTime='2008-09-15',
            releaseTime='2009-01-01',
            recordingStudios='Studio A, Studio B',
            producer='Artistic Producer',
            mixer='Mixing Engineer',
            comments='Comments\n...',
            primaryStyle='Style'))

        self.driver.showsReleaseName('Album')
        self.driver.showsCompilation(False)
        self.driver.showsLeadPerformer('Artist')
        self.driver.showsArea('')
        self.driver.showsGuestPerformers('Guitar: Guitarist; Piano: Pianist')
        self.driver.showsLabelName('Label')
        self.driver.showsCatalogNumber('XXX123456789')
        self.driver.showsUpc('123456789999')
        self.driver.showsRecordingTime('2008-09-15')
        self.driver.showsReleaseTime('2009-01-01')
        self.driver.showsDigitalReleaseTime('')
        self.driver.showsRecordingStudios('Studio A, Studio B')
        self.driver.showsProducer('Artistic Producer')
        self.driver.showsMixer('Mixing Engineer')
        self.driver.showsComments('Comments\n...')
        self.driver.showsPrimaryStyle('Style')
        self.driver.showsMediaType('')
        self.driver.showsReleaseType('')

    def testIndicatesWhetherAlbumIsACompilation(self):
        self.page.display(build.album(compilation=False))
        self.driver.showsCompilation(False)

        self.page.display(build.album(compilation=True))
        self.driver.showsCompilation(True)

    def testDisablesLeadPerformerEditionWhenAlbumIsACompilation(self):
        self.page.display(build.album(compilation=True, leadPerformer='Album Artist'))
        self.driver.showsLeadPerformer('Various Artists', disabled=True)

    def testSignalsWhenPictureSelected(self):
        image = build.image()
        self.pictureSelector.selected = image

        self.page.display(build.album())
        pictureSelectedSignal = ValueMatcherProbe('picture selected', image)
        self.page.bind(pictureSelected=pictureSelectedSignal.received)

        self.driver.addPicture()
        self.check(pictureSelectedSignal)

    def testSignalsWhenRemovePictureButtonClicked(self):
        self.page.display(build.album())
        removePictureSignal = ValueMatcherProbe('remove picture')

        self.page.bind(removePicture=removePictureSignal.received)

        self.driver.removePicture()
        self.check(removePictureSignal)

    def testSignalsWhenAlbumMetadataEdited(self):
        self.page.display(build.album())
        albumChangedSignal = ValueMatcherProbe('album changed')

        self.page.bind(metadataChanged=albumChangedSignal.received)

        albumChangedSignal.expect(has_properties(releaseName='Title'))
        self.driver.changeReleaseName('Title')
        self.check(albumChangedSignal)

        albumChangedSignal.expect(has_properties(compilation=True))
        self.driver.toggleCompilation()
        self.check(albumChangedSignal)

        albumChangedSignal.expect(has_properties(compilation=False))
        self.driver.toggleCompilation()
        self.check(albumChangedSignal)

        albumChangedSignal.expect(has_properties(leadPerformer='Artist'))
        self.driver.changeLeadPerformer('Artist')
        self.check(albumChangedSignal)

        albumChangedSignal.expect(has_properties(
            guestPerformers=[('Guitar', 'Guitarist'), ('Guitar', 'Bassist'),
                             ('Piano', 'Pianist')]))
        self.driver.changeGuestPerformers('Guitar: Guitarist; Guitar: Bassist; Piano: Pianist')
        self.check(albumChangedSignal)

        albumChangedSignal.expect(has_properties(labelName='Label'))
        self.driver.changeLabelName('Label')
        self.check(albumChangedSignal)

        albumChangedSignal.expect(has_properties(catalogNumber='XXX12345678'))
        self.driver.changeCatalogNumber('XXX12345678')
        self.check(albumChangedSignal)

        albumChangedSignal.expect(has_properties(upc='123456789999'))
        self.driver.changeUpc('123456789999')
        self.check(albumChangedSignal)

        albumChangedSignal.expect(has_properties(comments='Comments\n...\n'))
        self.driver.addComments('Comments')
        self.driver.addComments('...')
        self.check(albumChangedSignal)

        albumChangedSignal.expect(has_properties(releaseTime='2009-01-01'))
        self.driver.changeReleaseTime('2009-01-01')
        self.check(albumChangedSignal)

        albumChangedSignal.expect(has_properties(recordingTime='2008-09-15'))
        self.driver.changeRecordingTime('2008-09-15')
        self.check(albumChangedSignal)

        albumChangedSignal.expect(has_properties(recordingStudios='Studios'))
        self.driver.changeRecordingStudios('Studios')
        self.check(albumChangedSignal)

        albumChangedSignal.expect(has_properties(producer='Producer'))
        self.driver.changeProducer('Producer')
        self.check(albumChangedSignal)

        albumChangedSignal.expect(has_properties(mixer='Mixer'))
        self.driver.changeMixer('Mixer')
        self.check(albumChangedSignal)

        albumChangedSignal.expect(has_properties(primaryStyle='Jazz'))
        self.driver.selectPrimaryStyle('Jazz')
        self.check(albumChangedSignal)

        albumChangedSignal.expect(has_properties(primaryStyle='Custom'))
        self.driver.changePrimaryStyle('Custom')
        self.check(albumChangedSignal)