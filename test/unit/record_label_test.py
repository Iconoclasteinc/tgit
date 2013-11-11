# -*- coding: utf-8 -*-

import unittest
from flexmock import flexmock

from hamcrest import assert_that, contains, has_properties

from test.util import builders as build

from tgit.record_label import RecordLabel
from tgit.album import Album


class RecordLabelTest(unittest.TestCase):
    def setUp(self):
        self.catalog = flexmock()
        self.portfolio = flexmock()
        self.label = RecordLabel(self.portfolio, self.catalog)

    def testAddsNewAlbumToPortfolio(self):
        self.portfolio.should_receive('add').with_args(Album)

    def testLoadsTracksToAlbumInOrder(self):
        self.catalog.should_receive('load').with_args('my favorite things').and_return(
            build.track(filename='my favorite things', trackTitle='My Favorite Things'))
        self.catalog.should_receive('load').with_args('summertime').and_return(
            build.track(filename='summertime', trackTitle='Summertime'))

        album = build.album()
        self.label.addTrackToAlbum(album, 'my favorite things')
        self.label.addTrackToAlbum(album, 'summertime')

        assert_that(album.tracks,
                    contains(has_properties(filename='my favorite things',
                                            trackTitle='My Favorite Things'),
                             has_properties(filename='summertime', trackTitle='Summertime')),
                    'album tracks')

    def testSavesAllTracksInAlbum(self):
        timeOut = build.album(releaseName='Time Out')

        takeFive = build.track(filename='take five', trackTitle='Take Five')
        timeOut.addTrack(takeFive)
        pickUpSticks = build.track(filename='pick up sticks', trackTitle='Pick Up Sticks')
        timeOut.addTrack(pickUpSticks)

        self.catalog.should_receive('save').with_args(takeFive).once()
        self.catalog.should_receive('save').with_args(pickUpSticks).once()

        self.label.recordAlbum(timeOut)

