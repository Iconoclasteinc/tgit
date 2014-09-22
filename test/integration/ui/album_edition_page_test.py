# -*- coding: utf-8 -*-
import timeit
from hamcrest import has_entries, assert_that, less_than
from tgit.util import sip_api
sip_api.use_v2()

from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe
from test.drivers import AlbumEditionPageDriver
from test.integration.ui import ViewTest
from test.util import resources, builders as build
from tgit.metadata import Image
from tgit.ui.album_edition_page import AlbumEditionPage
from tgit.util import fs


class AlbumEditionPageTest(ViewTest):
    def render(self, album):
        self.page = AlbumEditionPage(album)
        self.page.refresh()
        self.driver = self.createDriverFor(self.page)
        self.show(self.page)

    def createDriverFor(self, widget):
        return AlbumEditionPageDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysPicturePlaceholderWhenAlbumHasNoCover(self):
        self.render(build.album())
        self.driver.showsPicturePlaceholder()

    def testDisplaysMainAlbumCoverWhenExisting(self):
        self.render(
            build.album(images=[build.image('image/jpeg', loadTestImage('front-cover.jpg'), Image.FRONT_COVER)]))
        self.driver.showsPicture()

    def testDisplaysAlbumMetadata(self):
        self.render(build.album(
            releaseName='Album',
            leadPerformer='Artist',
            isni='123456789',
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
        self.driver.showsISNI('123456789', True)
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
        album = build.album(compilation=False)
        self.render(album)
        self.driver.showsCompilation(False)

        album.compilation = True
        self.page.refresh()
        self.driver.showsCompilation(True)

    def testDisablesLeadPerformerEditionWhenAlbumIsACompilation(self):
        self.render(build.album(compilation=True, leadPerformer='Album Artist'))
        self.driver.showsLeadPerformer('Various Artists', disabled=True)

    def testTogglesLookupISNIButtonWhenAlbumIsNoLongerACompilation(self):
        album = build.album(compilation=True, leadPerformer='Album Artist')
        self.render(album)
        self.driver.enablesISNILookup(False)

        album.compilation = False
        self.page.refresh()
        self.driver.enablesISNILookup()

    def testDisablesLookupISNIButtonWhenAlbumIsACompilation(self):
        self.render(build.album(compilation=True, leadPerformer='Album Artist'))
        self.driver.enablesISNILookup(False)

    def testDisablesLookupISNIButtonWhenLeadPerformerIsEmpty(self):
        self.render(build.album(leadPerformer=''))
        self.driver.enablesISNILookup(False)

    def testDisablesLookupISNIButtonWhenLeadPerformerIsBlank(self):
        self.render(build.album(leadPerformer='     '))
        self.driver.enablesISNILookup(False)

    def testEnablesAssignISNIButtonWhenLeadPerformerIsNotEmpty(self):
        self.render(build.album(leadPerformer='performer'))
        self.driver.enablesISNIAssign()

    def testDisablesAssignISNIButtonWhenLeadPerformerIsNotEmpty(self):
        self.render(build.album())
        self.driver.enablesISNIAssign(False)

    def testSignalsWhenPictureSelected(self):
        self.render(build.album())

        selectPictureSignal = ValueMatcherProbe('select picture')
        self.page.selectPicture.connect(selectPictureSignal.received)

        self.driver.addPicture()
        self.check(selectPictureSignal)

    def testSignalsWhenAddingAPerformer(self):
        self.render(build.album())

        addPerformerSignal = ValueMatcherProbe('add performer')
        self.page.addPerformer.connect(addPerformerSignal.received)

        self.driver.addPerformer()
        self.check(addPerformerSignal)

    def testEfficientlyDisplaysImageCoverWhenItDoesNotChange(self):
        self.render(build.album(images=[build.image('image/jpeg', loadTestImage('big-image.jpg'), Image.FRONT_COVER)]))

        time = timeit.timeit(lambda: self.page.refresh(), number=50)
        assert_that(time, less_than(1), 'time to execute render 50 times')

    def testSignalsWhenRemovePictureButtonClicked(self):
        self.render(build.album())

        removePictureSignal = ValueMatcherProbe('remove picture')
        self.page.removePicture.connect(removePictureSignal.received)

        self.driver.removePicture()
        self.check(removePictureSignal)

    def testSignalsWhenLookupISNIButtonClicked(self):
        self.render(build.album(leadPerformer='performer'))

        lookupISNISignal = ValueMatcherProbe('lookup ISNI')
        self.page.lookupISNI.connect(lookupISNISignal.received)

        self.driver.lookupISNI()
        self.check(lookupISNISignal)

    def testSignalsWhenClearISNIButtonClicked(self):
        self.render(build.album(isni='0000123456789'))

        clearISNISignal = ValueMatcherProbe('clear ISNI')
        self.page.clearISNI.connect(clearISNISignal.received)

        self.driver.clearISNI()
        self.check(clearISNISignal)

    def testSignalsWhenAssignISNIButtonClicked(self):
        self.render(build.album(leadPerformer='performer'))

        assignISNISignal = ValueMatcherProbe('assign ISNI')
        self.page.assignISNI.connect(assignISNISignal.received)

        self.driver.assignISNI()
        self.check(assignISNISignal)

    def testSignalsWhenAlbumMetadataEdited(self):
        self.render(build.album())

        metadataChangedSignal = ValueMatcherProbe('metadata changed')
        self.page.metadataChanged.connect(metadataChangedSignal.received)

        metadataChangedSignal.expect(has_entries(releaseName='Title'))
        self.driver.changeReleaseName('Title')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(compilation=True))
        self.driver.toggleCompilation()
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(compilation=False))
        self.driver.toggleCompilation()
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(leadPerformer='Artist'))
        self.driver.changeLeadPerformer('Artist')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(
            guestPerformers=[('Guitar', 'Guitarist'), ('Guitar', 'Bassist'), ('Piano', 'Pianist')]))
        self.driver.changeGuestPerformers('Guitar: Guitarist; Guitar: Bassist; Piano: Pianist')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(labelName='Label'))
        self.driver.changeLabelName('Label')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(catalogNumber='XXX12345678'))
        self.driver.changeCatalogNumber('XXX12345678')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(upc='123456789999'))
        self.driver.changeUpc('123456789999')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(comments='Comments\n...\n'))
        self.driver.addComments('Comments')
        self.driver.addComments('...')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(releaseTime='2009-01-01'))
        self.driver.changeReleaseTime('2009-01-01')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(recordingTime='2008-09-15'))
        self.driver.changeRecordingTime('2008-09-15')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(recordingStudios='Studios'))
        self.driver.changeRecordingStudios('Studios')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(producer='Producer'))
        self.driver.changeProducer('Producer')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(mixer='Mixer'))
        self.driver.changeMixer('Mixer')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(primaryStyle='Jazz'))
        self.driver.selectPrimaryStyle('Jazz')
        self.check(metadataChangedSignal)

        metadataChangedSignal.expect(has_entries(primaryStyle='Custom'))
        self.driver.changePrimaryStyle('Custom')
        self.check(metadataChangedSignal)


def loadTestImage(name):
    return fs.readContent(resources.path(name))