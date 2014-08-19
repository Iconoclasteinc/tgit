# -*- coding: utf-8 -*-
import unittest

from tgit.sources.isni import NameRegistry
import test.util.isni_database as server


class ISNITest(unittest.TestCase):
    def setUp(self):
        server.start()
        self.registry = NameRegistry(host='localhost', port=5000)

    def tearDown(self):
        server.database.clear()
        server.stop()

    def testSampleQuery(self):
        server.database["00000001"] = [("Vincent", "Tence"), ("Vince", u"Tencé"), ("Vincent", u"Tencé")]
        #server.database["00000002"] = [("Edouard", "Tencé")]

        identities = self.registry.searchByKeywords(u"vincent", u"tencé")

        print identities

        # assert_that(identities, contains(contains('00000001', 'Vincent', u'Tencé')))
