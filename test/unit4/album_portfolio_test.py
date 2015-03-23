# -*- coding: utf-8 -*-

import unittest
from flexmock import flexmock
from test.util4 import builders as build
from tgit4.album_portfolio import AlbumPortfolio


class AlbumPortfolioTest(unittest.TestCase):
    def setUp(self):
        self.portfolio = AlbumPortfolio()

    def testNotifiesListenersOfNewAlbums(self):
        album = build.album()
        listeners = [flexmock(), flexmock(), flexmock()]
        for listener in listeners:
            self.portfolio.addPortfolioListener(listener)
            listener.should_receive('albumCreated').with_args(album).once()

        self.portfolio.addAlbum(album)