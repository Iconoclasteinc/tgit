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

    def testSavesAllTracksInAlbum(self):
        timeOut = build.album()

        takeFive = build.track()
        timeOut.addTrack(takeFive)
        pickUpSticks = build.track()
        timeOut.addTrack(pickUpSticks)

        self.catalog.should_receive('save').with_args(takeFive).once()
        self.catalog.should_receive('save').with_args(pickUpSticks).once()

        self.label.recordAlbum(timeOut)

