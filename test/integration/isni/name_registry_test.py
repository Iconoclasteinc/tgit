# -*- coding: utf-8 -*-
import unittest
from hamcrest import assert_that, contains, has_item, equal_to, greater_than

from tgit.sources.isni import NameRegistry
import test.util.isni_database as server


class ISNITest(unittest.TestCase):
    @unittest.skip('Exploration test')
    def testFindsIndentity(self):
        server.start()
        server.database["00000001"] = [(u"Joel", u"Miller"), (u"Joel E.", u"Miller"), (u"Joel", u"miller")]
        self.registry = NameRegistry(host='localhost', port=5000)
        identities = self.registry.searchByKeywords(u"joel", u"miller")
        server.database.clear()
        server.stop()

        assert_that(identities, contains(contains('00000001', u'Joel', u'Miller')))

    def testFindsRebeccaAnnMaloyIndentity(self):
        registry = NameRegistry(host='isni.oclc.nl')
        _, identities = registry.searchByKeywords(u"maloy", u"rebecca", u"ann")

        assert_that(identities, has_item(('0000000115677274', (u'Rebecca Ann', u'Maloy'))))

    def testFindsOnlyOneRecordWhenSearchingForRebeccaAnnMaloyIndentity(self):
        registry = NameRegistry(host='isni.oclc.nl')
        numberOfResults, _ = registry.searchByKeywords(u"maloy", u"rebecca", u"ann")

        assert_that(numberOfResults, equal_to('1'))

    def testFindsRebeccaAnnMaloyIndentityUsingPartOfHerName(self):
        registry = NameRegistry(host='isni.oclc.nl')
        _, identities = registry.searchByKeywords(u"malo", u"reb", u"a")

        assert_that(identities, has_item(('0000000115677274', (u'Rebecca Ann', u'Maloy'))))

    def testFindsMoreThanTwentyMatchesWhenSearchingForJoMiller(self):
        registry = NameRegistry(host='isni.oclc.nl')
        numberOfRecords, _ = registry.searchByKeywords(u"Miller", u"Jo")

        assert_that(int(numberOfRecords), greater_than(20))

    @unittest.skip('Exploration test')
    def testFindsMetallicaIdentity(self):
        registry = NameRegistry(host='isni.oclc.nl')
        identities = registry.searchByKeywords(u"Metallica")

        assert_that(identities, contains(contains('0000000122939631')))

    @unittest.skip('Exploration test')
    def testFindsTheBeatlesIdentity(self):
        registry = NameRegistry(host='isni.oclc.nl')
        identities = registry.searchByKeywords(u"Beatles", u"The")

        assert_that(identities, contains(contains('0000000121707484')))

    @unittest.skip('Exploration test')
    def testFindsTheBeatlesIdentityWithPrefixSentFirst(self):
        registry = NameRegistry(host='isni.oclc.nl')
        identities = registry.searchByKeywords(u"The", u"Beatles")

        assert_that(identities, contains(contains('0000000121707484')))
