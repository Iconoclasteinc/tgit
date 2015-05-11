# -*- coding: utf-8 -*-

import unittest

from hamcrest import contains
from hamcrest import assert_that

from test.test_signal import Subscriber
from test.util import builders as build
from tgit.album_portfolio import AlbumPortfolio


class AlbumPortfolioTest(unittest.TestCase):
    def setUp(self):
        self.portfolio = AlbumPortfolio()

    def test_notifies_listeners_of_new_albums(self):
        album = build.album()
        subscriber = Subscriber()

        self.portfolio.album_created.subscribe(subscriber)
        self.portfolio.add_album(album)

        assert_that(subscriber.events, contains(album), 'albums created')