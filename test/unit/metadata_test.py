# -*- coding: utf-8 -*-

import unittest
from hamcrest import assert_that, equal_to, has_entry, contains, has_property, contains_inanyorder
from hamcrest.library.collection.is_empty import empty

from tgit.metadata import Metadata, Image


class MetadataTest(unittest.TestCase):

    def testMissingMetadataIsConsideredEmpty(self):
        metadata = Metadata()
        assert_that(metadata['unknown'], equal_to(u''), 'missing value')

    def testDropsAllTagsAndImagesWhenCleared(self):
        metadata = Metadata()
        metadata['tag'] = 'value'
        metadata.addImage('img/jpeg', '...')

        metadata.clear()
        assert_that(metadata, empty(), 'tags')
        assert_that(list(metadata.images), empty(), 'images')

    def testReplacesTagsAndImagesWhenMerged(self):
        metadata = Metadata()
        metadata['tag'] = 'original'
        metadata['other'] = 'value'
        metadata.addImage('img/jpeg', 'image content')

        other = Metadata()
        other['tag'] = 'replaced'
        other.addImage('img/png', 'other image')

        metadata.merge(other)
        assert_that(metadata, has_entry('tag', 'replaced'), 'tags')
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