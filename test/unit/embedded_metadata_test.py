# -*- coding: utf-8 -*-

import unittest

from flexmock import flexmock
from hamcrest import assert_that, equal_to

from test.util import builders as build
from tgit.embedded_metadata import EmbeddedMetadata
from tgit.track import Track


class EmbeddedMetadataTest(unittest.TestCase):
    def setUp(self):
        self.container = flexmock()
        self.library = EmbeddedMetadata(self.container)

    def testLoadsTrackMetadataFromContainer(self):
        metadata = build.metadata(trackTitle='Summertime',
                                  releaseName='My Favorite Things',
                                  images=[('image/jpeg', 'Front Cover', 'data')])

        self.container.should_receive('load').with_args('summertime.mp3').and_return(metadata)
        track = self.library.fetch('summertime.mp3')
        assert_that(track.metadata, equal_to(metadata), 'track metadata')

    def testSavesTrackMetadataToContainer(self):
        metadata = build.metadata(trackTitle='Summertime',
                                  releaseName='My Favorite Things',
                                  images=[('image/jpeg', 'Front Cover', 'data')])

        self.container.should_receive('save').with_args('summertime.mp3', metadata).once()
        self.library.store(Track('summertime.mp3', metadata))