# -*- coding: utf-8 -*-
import unittest

from lxml import etree

from hamcrest import assert_that, contains, has_item, equal_to, greater_than, not_none, anything
import requests

from tgit.isni.name_registry import NameRegistry
import test.util.isni_database as server


def has_identity(isni=anything(), name=anything()):
    return has_item(contains(isni, contains(name, anything(), anything())))


class ISNITest(unittest.TestCase):
    @unittest.skip('Exploration test')
    def testFindsIndentity(self):
        server.start()
        server.database["00000001"] = [("Joel", "Miller"), ("Joel E.", "Miller"), ("Joel", "miller")]
        self.registry = NameRegistry(host='localhost', port=5000)
        identities = self.registry.searchByKeywords("joel", "miller")
        server.database.clear()
        server.stop()

        assert_that(identities, has_identity('00000001', 'Joel Miller'))

    def testFindsRebeccaAnnMaloyIdentity(self):
        registry = NameRegistry(host='isni.oclc.nl')
        _, identities = registry.searchByKeywords("maloy", "rebecca", "ann")

        assert_that(identities, has_identity('0000000115677274', 'Rebecca Ann Maloy'))

    def testFindsOnlyOneRecordWhenSearchingForRebeccaAnnMaloyIndentity(self):
        registry = NameRegistry(host='isni.oclc.nl')
        numberOfResults, _ = registry.searchByKeywords("maloy", "rebecca", "ann")

        assert_that(numberOfResults, equal_to('1'))

    def testFindsRebeccaAnnMaloyIndentityUsingPartOfHerName(self):
        registry = NameRegistry(host='isni.oclc.nl')
        _, identities = registry.searchByKeywords("malo", "reb", "a")

        assert_that(identities, has_identity('0000000115677274', 'Rebecca Ann Maloy'))

    def testFindsJoelMillerIndentityWithDates(self):
        registry = NameRegistry(host='isni.oclc.nl')
        _, identities = registry.searchByKeywords("miller", "joel")

        assert_that(identities, has_identity('0000000073759369', 'Joel Miller'))

    def testFindsMoreThanTwentyMatchesWhenSearchingForJoMiller(self):
        registry = NameRegistry(host='isni.oclc.nl')
        numberOfRecords, _ = registry.searchByKeywords("Miller", "Jo")

        assert_that(int(numberOfRecords), greater_than(20))

    def testFindsMetallicaIdentity(self):
        registry = NameRegistry(host='isni.oclc.nl')
        _, identities = registry.searchByKeywords("Metallica")

        assert_that(identities, has_identity('0000000122939631', 'Metallica'))

    def testFindsTheBeatlesIdentity(self):
        registry = NameRegistry(host='isni.oclc.nl')
        _, identities = registry.searchByKeywords("Beatles", "The")

        assert_that(identities, has_identity('0000000121707484', 'The Beatles'))

    def testFindsTheBeatlesIdentityWithPrefixSentFirst(self):
        registry = NameRegistry(host='isni.oclc.nl')
        _, identities = registry.searchByKeywords("The", "Beatles")

        title = 'The fool on the hill from The Beatles\' T.V. film Magical mystery tour'
        assert_that(identities, has_identity('0000000121707484', 'The Beatles'))

    def testFindsLedZeppelinIdentity(self):
        registry = NameRegistry(host='isni.oclc.nl')
        _, identities = registry.searchByKeywords("Led", "Zeppelin")

        assert_that(identities, has_identity('0000000123483226', 'Led Zeppelin'))

    def testFindsLedZeppelinIdentityWithPrefixSentFirst(self):
        registry = NameRegistry(host='isni.oclc.nl')
        _, identities = registry.searchByKeywords("Zeppelin", "Led")

        assert_that(identities, has_identity('0000000123483226', 'Led Zeppelin'))

    def testFindsRageAgainstTheMachineIdentity(self):
        registry = NameRegistry(host='isni.oclc.nl')
        _, identities = registry.searchByKeywords("Rage", "Against", "The", "Machine")

        assert_that(identities, has_identity('0000000122905407', 'Rage against the machine'))

    def testFindsRageAgainstTheMachineWithPrefixSentFirst(self):
        registry = NameRegistry(host='isni.oclc.nl')
        _, identities = registry.searchByKeywords("Machine", "Rage", "Against", "The")

        assert_that(identities, has_identity('0000000122905407', 'Rage against the machine'))

    @unittest.skip('ISNI Response changes too often for test to be valid')
    def testAssignWithTheISNIAtomPubAPIUsingAMinimalRequest(self):
        url = 'https://isni-m-acc.oclc.nl/ATOM/isni'
        payload = '''
            <Request>
                <requestID>
                    <dateTimeOfRequest>2011-05-20T09:09:35.5063705+02:00</dateTimeOfRequest>
                    <requestorTransactionId>5340</requestorTransactionId>
                </requestID>
                <identityInformation>
                    <requestorIdentifierOfIdentity>
                        <referenceURI>http://www.sos.nl</referenceURI>
                        <identifier>13365</identifier>
                    </requestorIdentifierOfIdentity>
                    <identity>
                        <personOrFiction>
                            <personalName>
                                <nameUse>public and private</nameUse>
                                <surname>BAERTHEL</surname>
                                <forename>JAN</forename>
                            </personalName>
                            <resource>
                                <creationClass>
                                    <domain>literature </domain>
                                    <formOfPublication>book </formOfPublication>
                                    <pietjePuk>fi<p>lm</p></pietjePuk>
                                </creationClass>
                                <creationRole>aut</creationRole>
                                <titleOfWork>
                                    <title>Industrielles Bauen: Leitfaden f??MU-Gesch?sf??r</title>
                                </titleOfWork>
                            </resource>
                        </personOrFiction>
                    </identity>
                </identityInformation>
            </Request>
        '''
        headers = {'content-type': 'application/atom+xml'}
        response = requests.post(url, data=payload, headers=headers, verify=False)
        assert_that(response.status_code, equal_to(requests.codes.ok), 'response code')

        results = etree.fromstring(response.content)
        assert_that(results.find('ISNIAssigned'), not_none(), 'response code')

    @unittest.skip('Exploration test')
    def testAssignWithTheISNIAtomPubAPIUsingAnInvalidRequest(self):
        url = 'https://isni-m-acc.oclc.nl/ATOM/isni'
        payload = '''
            <Request>
                <requestID>
                    <dateTimeOfRequest>2011-05-20T09:09:35.5063705+02:00</dateTimeOfRequest>
                    <requestorTransactionId>5340</requestorTransactionId>
                </requestID>
                <identityInformation>
                    <requestorIdentifierOfIdentity>
                        <referenceURI>http://www.sos.nl</referenceURI>
                        <identifier>13365</identifier>
                    </requestorIdentifierOfIdentity>
                    <identity>
                        <personOrFiction>
                            <resource>
                                <creationClass>
                                    <domain>literature </domain>
                                    <formOfPublication>book </formOfPublication>
                                    <pietjePuk>fi<p>lm</p></pietjePuk>
                                </creationClass>
                                <creationRole>aut</creationRole>
                                <titleOfWork>
                                    <title>Industrielles Bauen: Leitfaden f??MU-Gesch?sf??r</title>
                                </titleOfWork>
                            </resource>
                        </personOrFiction>
                    </identity>
                </identityInformation>
            </Request>
        '''
        headers = {'content-type': 'application/atom+xml'}
        response = requests.post(url, data=payload, headers=headers, verify=False)
        content = response.content
        assert_that(response.status_code, equal_to(requests.codes.ok), 'response code')

        results = etree.fromstring(content)
        noIsni = results.find('noISNI')
        assert_that(noIsni, not_none(), 'no ISNI tag')

        sparse = noIsni.find('reason')
        assert_that(sparse.text, equal_to('invalidFormat'), 'invalid response')

    @unittest.skip('Exploration test')
    def testAssignOrganisationWithTheISNIAtomPubAPIUsingASparseRequest(self):
        url = 'https://isni-m-acc.oclc.nl/ATOM/isni'
        payload = '''
        <Request xsi:noNamespaceSchemaLocation="ISNI%20request.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <requestID>
                <dateTimeOfRequest>2001-12-17T09:30:47Z</dateTimeOfRequest>
                <requestorTransactionId>text</requestorTransactionId>
            </requestID>
            <identityInformation>
                <requestorIdentifierOfIdentity>
                    <referenceURI>www.ragaddress.com</referenceURI>
                    <identifier>234234234</identifier>
                </requestorIdentifierOfIdentity>
                <identity>
                    <organisation>
                        <organisationType>Musical group or band</organisationType>
                        <organisationName>
                            <mainName>We are the best</mainName>
                        </organisationName>
                    </organisation>
                </identity>
            </identityInformation>
        </Request>
        '''
        headers = {'content-type': 'application/atom+xml'}
        response = requests.post(url, data=payload, headers=headers, verify=False)
        content = response.content
        assert_that(response.status_code, equal_to(requests.codes.ok), 'response code')

        results = etree.fromstring(content)
        noIsni = results.find('noISNI')
        assert_that(noIsni, not_none(), 'no ISNI tag')

        sparse = noIsni.find('reason')
        assert_that(sparse.text, equal_to('sparse'), 'sparse response')

    @unittest.skip('Exploration test')
    def testAssignPersonWithTheISNIAtomPubAPIUsingASparseRequest(self):
        url = 'https://isni-m-acc.oclc.nl/ATOM/isni'
        payload = '''
            <Request xsi:noNamespaceSchemaLocation="ISNI%20request.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <requestID>
                    <dateTimeOfRequest>2001-12-17T09:30:47Z</dateTimeOfRequest>
                    <requestorTransactionId>My ID</requestorTransactionId>
                </requestID>
                <identityInformation>
                    <requestorIdentifierOfIdentity>
                        <referenceURI>www.rag.address.com</referenceURI>
                        <identifier>1515161634</identifier>
                    </requestorIdentifierOfIdentity>
                    <otherIdentifierOfIdentity>
                        <identifier>99667784</identifier>
                        <type>IPD</type>
                    </otherIdentifierOfIdentity>
                    <identity>
                        <personOrFiction>
                            <personalName>
                                <nameUse>public and private</nameUse>
                                <surname>Nieuwname</surname>
                                <forename>Pamela Williams</forename>
                            </personalName>
                            <personalNameVariant>
                                <nameUse>private</nameUse>
                                <surname>Williams</surname>
                                <forename>Pamela Jane</forename>
                            </personalNameVariant>
                        </personOrFiction>
                    </identity>
                </identityInformation>
                <isRelated identityType="personOrFiction">
                    <relationType>co-author</relationType>
                    <noISNI>
                        <PPN>082588929</PPN>
                        <personalName>
                            <nameUse>public</nameUse>
                            <surname>Williams</surname>
                            <forename>Selma R.</forename>
                        </personalName>
                    </noISNI>
                </isRelated>
            </Request>
        '''
        headers = {'content-type': 'application/atom+xml'}
        response = requests.post(url, data=payload, headers=headers, verify=False)
        assert_that(response.status_code, equal_to(requests.codes.ok), 'response code')

        content = response.content
        results = etree.fromstring(content)
        noIsni = results.find('noISNI')
        assert_that(noIsni, not_none(), 'no ISNI tag')

        sparse = noIsni.find('reason')
        assert_that(sparse.text, equal_to('sparse'), 'sparse response')

    @unittest.skip('Exploration test')
    def testAssignPersonWithTheISNIAtomPubAPIUsingAPossibleMatchesRequestReturningScoreOf06(self):
        url = 'https://isni-m-acc.oclc.nl/ATOM/isni'
        payload = '''
            <Request xsi:noNamespaceSchemaLocation="ISNI%20request.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <requestID>
                    <dateTimeOfRequest>2012-11-09T09:30:47Z</dateTimeOfRequest>
                    <requestorTransactionId>multiple match1</requestorTransactionId>
                </requestID>
                <identityInformation>
                    <requestorIdentifierOfIdentity>
                        <referenceURI>myURL</referenceURI>
                        <identifier>11112222332323</identifier>
                    </requestorIdentifierOfIdentity>
                    <identity>
                        <personOrFiction>
                            <personalName>
                                <nameUse>public and private</nameUse>
                                <surname>Adler</surname>
                                <forename>Larry</forename>
                            </personalName>
                            <birthDate>1914</birthDate>
                            <deathDate>2001</deathDate>
                            <resource>
                                <creationClass>jm</creationClass>
                                <creationRole>prf</creationRole>
                                <titleOfWork>
                                    <title>St. Louis blues</title>
                                </titleOfWork>
                            </resource>
                            <resource>
                                <creationClass>jm</creationClass>
                                <creationRole>prf</creationRole>
                                <titleOfWork>
                                    <title>Beguine</title>
                                </titleOfWork>
                            </resource>
                        </personOrFiction>
                    </identity>
                    <note>should return possible match with PPNs 37444949X, 36586272X and 083863184</note>
                </identityInformation>
            </Request>
        '''
        headers = {'content-type': 'application/atom+xml'}
        response = requests.post(url, data=payload, headers=headers, verify=False)
        assert_that(response.status_code, equal_to(requests.codes.ok), 'response code')

        content = response.content
        results = etree.fromstring(content)
        noIsni = results.find('noISNI')
        assert_that(noIsni, not_none(), 'no ISNI tag')

        sparse = noIsni.find('reason')
        assert_that(sparse.text, equal_to('possibleMatch'), 'possible matches response')

    @unittest.skip('Exploration test')
    def testAssignPersonWithTheISNIAtomPubAPIUsingAPossibleMatchesRequestReturningScoreOf085(self):
        url = 'https://isni-m-acc.oclc.nl/ATOM/isni'
        payload = '''
            <Request xsi:noNamespaceSchemaLocation="ISNI%20request.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <requestID>
                    <dateTimeOfRequest>2012-11-09T09:30:47Z</dateTimeOfRequest>
                    <requestorTransactionId>multiple match1</requestorTransactionId>
                </requestID>
                <identityInformation>
                    <requestorIdentifierOfIdentity>
                        <referenceURI>myURL</referenceURI>
                        <identifier>11112222332558</identifier>
                    </requestorIdentifierOfIdentity>
                    <identity>
                        <personOrFiction>
                            <personalName>
                                <nameUse>public and private</nameUse>
                                <surname>Adams</surname>
                                <forename>John</forename>
                            </personalName>
                            <birthDate>1947</birthDate>
                            <resource>
                                <creationClass>txt</creationClass>
                                <creationRole>aut</creationRole>
                                <titleOfWork>
                                    <title>Common tones in simple time</title>
                                </titleOfWork>
                            </resource>
                        </personOrFiction>
                    </identity>
                    <note>trying to get low score matches with 121312917, 025525212, 038373734, 036219002, 114367671, 107884143</note>
                </identityInformation>
            </Request>
        '''
        headers = {'content-type': 'application/atom+xml'}
        response = requests.post(url, data=payload, headers=headers, verify=False)
        assert_that(response.status_code, equal_to(requests.codes.ok), 'response code')

        content = response.content
        results = etree.fromstring(content)
        noIsni = results.find('noISNI')
        assert_that(noIsni, not_none(), 'no ISNI tag')

        sparse = noIsni.find('reason')
        assert_that(sparse.text, equal_to('possibleMatch'), 'possible matches response')

    @unittest.skip('ISNI Response changes too often for test to be valid')
    def testAssignAnISNIUsingFullNameAndTitleOfWorks(self):
        registry = NameRegistry(assignHost='isni-m-acc.oclc.nl')
        isni = registry.assign("Jan", "Baerthel", "Industrielles Bauen: Leitfaden", "Industrielles Bauen")

        assert_that(isni, equal_to('0000000124568061'))