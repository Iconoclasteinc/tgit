# -*- coding: utf-8 -*-
import unittest

from hamcrest import assert_that, contains, has_item, equal_to, greater_than
import requests

from tgit.isni.name_registry import NameRegistry
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

        title = u'Scolica enchiriadis and the non-diatonic plainsong tradition. -'
        assert_that(identities, has_item(('0000000115677274', (u'Rebecca Ann', u'Maloy', '', title))))

    def testFindsOnlyOneRecordWhenSearchingForRebeccaAnnMaloyIndentity(self):
        registry = NameRegistry(host='isni.oclc.nl')
        numberOfResults, _ = registry.searchByKeywords(u"maloy", u"rebecca", u"ann")

        assert_that(numberOfResults, equal_to('1'))

    def testFindsRebeccaAnnMaloyIndentityUsingPartOfHerName(self):
        registry = NameRegistry(host='isni.oclc.nl')
        _, identities = registry.searchByKeywords(u"malo", u"reb", u"a")

        title = u'Scolica enchiriadis and the non-diatonic plainsong tradition. -'
        assert_that(identities, has_item(('0000000115677274', (u'Rebecca Ann', u'Maloy', '', title))))

    def testFindsJoelMillerIndentityWithDates(self):
        registry = NameRegistry(host='isni.oclc.nl')
        _, identities = registry.searchByKeywords(u"miller", u"joel")

        title = u'--and then everything started to look different--'
        assert_that(identities, has_item(('0000000073759369', (u'Joel', u'Miller', u'1969-', title))))

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

    @unittest.skip('Exploration test')
    def testCommunicateWithTheISNIAtomPubAPI(self):
        url = 'https://isni-m-acc.oclc.nl:2600/ATOM/isni'
        payload = '<?xml version="1.0" ?><entry xmlns="http://www.w3.org/2005/Atom"><Request></Request></entry>'
        headers = {'content-type': 'application/atom+xml'}
        response = requests.post(url, data=payload, headers=headers, verify=False)
        content = response.text
        assert_that(response.status_code, equal_to(requests.codes.ok), 'response code')
