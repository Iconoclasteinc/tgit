# -*- coding: utf-8 -*-
from hamcrest import has_properties

# noinspection PyUnresolvedReferences
import use_sip_api_v2

from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe
from test.drivers import AlbumEditionPageDriver
from test.integration.ui import ViewTest
from test.util import resources, builders as build

from tgit.ui.views.album_edition_page import AlbumEditionPage
from tgit.util import fs


def loadImage(name):
    return fs.readContent(resources.path(name))


class AlbumEditionPageTest(ViewTest):
    def setUp(self):
        super(AlbumEditionPageTest, self).setUp()
        self.view = AlbumEditionPage()
        self.widget = self.view.render()
        self.show(self.widget)
        self.driver = self.createDriverFor(self.widget)

    def createDriverFor(self, widget):
        return AlbumEditionPageDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysPicturePlaceholderForAlbumWithoutCover(self):
        album = build.album()
        self.view.show(album)
        self.driver.showsPicturePlaceholder()

    def testDisplaysMainAlbumCover(self):
        album = build.album()
        album.addFrontCover('image/jpeg', loadImage('front-cover.jpg'))
        self.view.show(album)
        self.driver.showsPicture()

    def testDisplaysAlbumMetadata(self):
        album = build.album(
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
            primaryStyle='Style')

        self.view.show(album)

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
        album = build.album()
        self.view.show(album)
        self.driver.showsCompilation(False)

        album.compilation = True
        self.view.show(album)
        self.driver.showsCompilation(True)

        album.compilation = False
        self.view.show(album)
        self.driver.showsCompilation(False)

    def testSignalsWhenAddPictureButtonClicked(self):
        self.view.show(build.album())

        addPictureSignal = ValueMatcherProbe('add picture')

        class AddPictureListener(object):
            def addPicture(self):
                addPictureSignal.received()

        self.view.announceTo(AddPictureListener())

        self.driver.addPicture()
        self.check(addPictureSignal)

    def testSignalsWhenRemovePictureButtonClicked(self):
        self.view.show(build.album())

        removePictureSignal = ValueMatcherProbe('remove picture')

        class RemovePictureListener(object):
            def removePicture(self):
                removePictureSignal.received()

        self.view.announceTo(RemovePictureListener())

        self.driver.removePicture()
        self.check(removePictureSignal)

    def testSignalsWhenAlbumMetadataEdited(self):
        self.view.show(build.album())

        changes = ValueMatcherProbe('album changed')

        class AlbumChangedListener(object):
            def metadataEdited(self, state):
                changes.received(state)

        self.view.announceTo(AlbumChangedListener())

        changes.expect(has_properties(releaseName='Title'))
        self.driver.changeReleaseName('Title')
        self.check(changes)

        changes.expect(has_properties(compilation=True))
        self.driver.toggleCompilation()
        self.check(changes)

        changes.expect(has_properties(compilation=False))
        self.driver.toggleCompilation()
        self.check(changes)

        changes.expect(has_properties(leadPerformer='Artist'))
        self.driver.changeLeadPerformer('Artist')
        self.check(changes)

        changes.expect(has_properties(
            guestPerformers=[('Guitar', 'Guitarist'), ('Guitar', 'Bassist'),
                             ('Piano', 'Pianist')]))
        self.driver.changeGuestPerformers('Guitar: Guitarist; Guitar: Bassist; Piano: Pianist')
        self.check(changes)

        changes.expect(has_properties(labelName='Label'))
        self.driver.changeLabelName('Label')
        self.check(changes)

        changes.expect(has_properties(catalogNumber='XXX12345678'))
        self.driver.changeCatalogNumber('XXX12345678')
        self.check(changes)

        changes.expect(has_properties(upc='123456789999'))
        self.driver.changeUpc('123456789999')
        self.check(changes)

        changes.expect(has_properties(comments='Comments\n...\n'))
        self.driver.addComments('Comments')
        self.driver.addComments('...')
        self.check(changes)

        changes.expect(has_properties(releaseTime='2009-01-01'))
        self.driver.changeReleaseTime('2009-01-01')
        self.check(changes)

        changes.expect(has_properties(recordingTime='2008-09-15'))
        self.driver.changeRecordingTime('2008-09-15')
        self.check(changes)

        changes.expect(has_properties(recordingStudios='Studios'))
        self.driver.changeRecordingStudios('Studios')
        self.check(changes)

        changes.expect(has_properties(producer='Producer'))
        self.driver.changeProducer('Producer')
        self.check(changes)

        changes.expect(has_properties(mixer='Mixer'))
        self.driver.changeMixer('Mixer')
        self.check(changes)

        changes.expect(has_properties(primaryStyle='Style'))
        self.driver.changePrimaryStyle('Style')
        self.check(changes)