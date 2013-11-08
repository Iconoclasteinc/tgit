# -*- coding: utf-8 -*-

import unittest
from hamcrest import (assert_that, equal_to, has_entries, contains, has_property,
                      contains_inanyorder, is_not, has_key, has_length, is_in, is_)
from hamcrest.library.collection.is_empty import empty

from tgit.metadata import Metadata, Image


class MetadataTest(unittest.TestCase):

    def testIsAMutableContainer(self):
        metadata = Metadata(artist='James Blunt')
        assert_that(metadata['artist'], equal_to('James Blunt'), 'accessed item')
        metadata['artist'] = 'Adele'
        assert_that(metadata['artist'], equal_to('Adele'), 'assigned item')
        metadata['album'] = 'Adele 21'
        assert_that(metadata, has_length(2), 'length')
        assert_that('artist', is_in(metadata), 'member')
        del metadata['artist']
        assert_that('title', is_not(is_in(metadata)), 'member')

    def testMissingTagIsConsideredEmpty(self):
        metadata = Metadata()
        assert_that(metadata['missing'], equal_to(u''), 'missing value')

    def testIsInitiallyEmpty(self):
        metadata = Metadata()

        assert_that(metadata, empty(), 'tags')
        assert_that(list(metadata.images), empty(), 'images')
        assert_that(metadata.empty(), is_(True), 'emptiness')

    def testIsNotEmptyWhenContainingImages(self):
        metadata = Metadata()
        metadata.addImage('img/jpeg', '...')

        assert_that(metadata.empty(), is_(False), 'emptiness')

    def testIsNotEmptyWhenHoldingTags(self):
        metadata = Metadata()
        metadata['artist'] = 'John Doe'
        metadata.addImage('img/jpeg', '...')

        assert_that(metadata.empty(), is_(False), 'emptiness')

    def testIsEmptyWhenCleared(self):
        metadata = Metadata()
        metadata['artist'] = 'John Doe'
        metadata.addImage('img/jpeg', '...')

        metadata.clear()
        assert_that(metadata.empty(), is_(True), 'emptiness')

    def testUpdatesTagsAndReplacesImagesWhenUpdated(self):
        metadata = Metadata()
        metadata['artist'] = 'Pascal Obispo'
        metadata['album'] = ''
        metadata.addImage('img/jpeg', 'missing')

        other = Metadata()
        other['album'] = "Un jour comme aujourd'hui"
        other.addImage('img/png', 'cover.png')

        metadata.update(other)
        assert_that(metadata, has_entries(artist='Pascal Obispo',
                                          album="Un jour comme aujourd'hui"), 'updated tags')
        assert_that(metadata.images, contains(has_property('data', 'cover.png')), 'updated images')

    def testCanReturnASelectionOfItsTagsWithImages(self):
        metadata = Metadata(artist='Alain Souchon', album=u"C'est déjà ça",
                            track='Foule sentimentale')
        metadata.addImage('img/jpeg', 'front-cover.jpg')
        metadata.addImage('img/jpeg', 'back-cover.jpg')

        selection = metadata.copy('artist', 'album', 'label')

        assert_that(selection, has_entries(artist='Alain Souchon',
                                           album=u"C'est déjà ça",
                                           label=''),
                    'selected tags')
        assert_that(selection, is_not(has_key('track')), 'selected tags')
        assert_that(selection.images, contains(has_property('data', 'front-cover.jpg'),
                                               has_property('data', 'back-cover.jpg')),
                    'selected images')

    def testLooksUpImagesByType(self):
        metadata = Metadata()
        metadata.addImage('img/jpeg', 'front-cover.jpg', Image.FRONT_COVER)
        metadata.addImage('img/png', 'front-cover.png', Image.FRONT_COVER)
        metadata.addImage('img/jpeg', 'back-cover.jpg', Image.BACK_COVER)

        assert_that(metadata.imagesOfType(Image.FRONT_COVER),
                    contains_inanyorder(has_property('data', 'front-cover.jpg'),
                                        has_property('data', 'front-cover.png')),
                    'front cover images')