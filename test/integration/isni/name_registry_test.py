# -*- coding: utf-8 -*-
import unittest
from hamcrest import assert_that, contains

from tgit.sources.isni import NameRegistry
import test.util.isni_database as server


class ISNITest(unittest.TestCase):
    def testFindsIndentity(self):
        server.start()
        server.database["00000001"] = [("Vincent", "Tence"), ("Vince", u"Tencé"), ("Vincent", u"Tencé")]
        self.registry = NameRegistry(host='localhost', port=5000)
        identities = self.registry.searchByKeywords(u"vincent", u"tencé")
        server.database.clear()
        server.stop()

        assert_that(identities, contains(contains('00000001', 'Vincent', u'Tencé')))

    def testFindsIndentityUsingRealIsniDatabase(self):
        registry = NameRegistry(host='isni.oclc.nl')
        identities = registry.searchByKeywords(u"miller", u"joel e.")

        assert_that(identities, contains(contains('0000000067123073', u'Joel E.', u'Miller')))