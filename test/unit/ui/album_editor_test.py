# -*- coding: utf-8 -*-
import unittest
from hamcrest import assert_that, equal_to, contains, has_properties
from test.util import builders as build, resources
from tgit.metadata import Image
from tgit.ui.album_editor import AlbumEditor
from tgit.util import fs


class AlbumEditorTest(unittest.TestCase):
    def setUp(self):
        self.album = build.album()
        self.editor = AlbumEditor(self.album)

    def testUpdatesAlbumMetadataOnEdition(self):
        class Snapshot(object):
            pass

        changes = Snapshot()
        changes.releaseName = 'Title'
        changes.leadPerformer = 'Artist'
        changes.guestPerformers = [('Guitar', 'Guitarist')]
        changes.labelName = 'Label'
        changes.catalogNumber = 'XXX123456789'
        changes.upc = '123456789999'
        changes.comments = 'Comments\n...'
        changes.releaseTime = '2009-01-01'
        changes.recordingTime = '2008-09-15'
        changes.recordingStudios = 'Studios'
        changes.producer = 'Producer'
        changes.mixer = 'Engineer'
        changes.primaryStyle = 'Style'

        self.editor.metadataEdited(changes)

        assert_that(self.album.releaseName, equal_to('Title'), 'release name')
        assert_that(self.album.leadPerformer, equal_to('Artist'), 'lead performer')
        assert_that(self.album.guestPerformers,
                    equal_to([('Guitar', 'Guitarist')]), 'guest performers')
        assert_that(self.album.labelName, equal_to('Label'), 'label name')
        assert_that(self.album.catalogNumber, equal_to('XXX123456789'), 'catalog number')
        assert_that(self.album.upc, equal_to('123456789999'), 'upc')
        assert_that(self.album.comments, equal_to('Comments\n...'), 'comments')
        assert_that(self.album.releaseTime, equal_to('2009-01-01'), 'release time')
        assert_that(self.album.recordingTime, equal_to('2008-09-15'), 'recording time')
        assert_that(self.album.recordingStudios, equal_to('Studios'), 'recording studios')
        assert_that(self.album.producer, equal_to('Producer'), 'producer')
        assert_that(self.album.mixer, equal_to('Engineer'), 'mixer')
        assert_that(self.album.primaryStyle, equal_to('Style'), 'primary style')

    def testRemovesAlbumImagesUponRequest(self):
        self.album.addFrontCover('image/jpeg', 'image data')
        self.editor.removePicture()
        assert_that(self.album.images, equal_to([]), 'images')

    def testReplacesAlbumImagesWithSelectedPicture(self):
        self.album.addFrontCover(mime='image/gif', data='old cover')
        selectedCover = resources.path('front-cover.jpg')
        self.editor.pictureSelected(selectedCover)

        assert_that(self.album.images, contains(has_properties(mime='image/jpeg',
                                                               data=contentOf(selectedCover),
                                                               type=Image.FRONT_COVER,
                                                               desc='Front Cover')), 'images')


def contentOf(name):
    return fs.readContent(name)