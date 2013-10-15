# -*- coding: utf-8 -*-

import unittest
from hamcrest import assert_that, equal_to, has_entry, contains, has_property, contains_inanyorder
from hamcrest.library.collection.is_empty import empty

from tgit.metadata import Metadata, Image


class MetadataTest(unittest.TestCase):
    def testMissingMetadataDefaultsToEmptyString(self):
        metadata = Metadata()
        assert_that(metadata['unknown'], equal_to(u''), 'missing value')

    def testDropsAllKeysAndImagesWhenCleared(self):
        metadata = Metadata()
        metadata['key'] = 'value'
        metadata.addImage('img/jpeg', '...')

        metadata.clear()
        assert_that(metadata, empty(), 'tags')
        assert_that(list(metadata.images), empty(), 'images')

    def testReplacesKeysAndImagesWhenOverwritten(self):
        metadata = Metadata()
        metadata['key'] = 'value'
        metadata.addImage('img/jpeg', 'image content')

        other = Metadata()
        other['key'] = 'other value'
        other.addImage('img/png', 'other image')

        metadata.copy(other)
        assert_that(metadata, has_entry('key', 'other value'), 'tags')
        assert_that(metadata.images, contains(has_property('data', 'other image')), 'images')

    def testLooksUpImagesByType(self):
        metadata = Metadata()
        metadata.addImage('img/jpeg', 'front-cover.jpg', Image.FRONT_COVER)
        metadata.addImage('img/png', 'front-cover.png', Image.FRONT_COVER)
        metadata.addImage('img/jpeg', 'back-cover.jpg', Image.BACK_COVER)

        assert_that(metadata.imagesOfType(Image.FRONT_COVER),
                    contains_inanyorder(has_property('data', 'front-cover.jpg'),
                                        has_property('data', 'front-cover.png')),
                    'front cover images')