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

    def testCommunicateWithTheISNIAtomPubAPIUsingAFullRequest(self):
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
                    <otherIdentifierOfIdentity>
                        <identifier>I-002043149-4</identifier>
                        <type>IPI</type>
                    </otherIdentifierOfIdentity>
                    <identity>
                        <personOrFiction>
                            <personalName>
                                <nameUse>public and private</nameUse>
                                <surname>BAERTHEL</surname>
                                <forename>JAN</forename>
                                <numeration>0</numeration>
                                <nameTitle>Sir</nameTitle>
                                <languageOfName>dut</languageOfName>
                                <script>Egyp</script>
                            </personalName>
                            <deathDate>2011-04-29</deathDate>
                            <instrumentAndVoice>sa</instrumentAndVoice>
                            <personalNameVariant>
                                <nameUse>public</nameUse>
                                <surname>Leiden</surname>
                                <forename>Jantje, van</forename>
                                <numeration>XIIV</numeration>
                                <nameTitle>Hee</nameTitle>
                            </personalNameVariant>
                            <birthDate>1973-02-05</birthDate>
                            <gender>male</gender>
                            <instrumentAndVoice>tb</instrumentAndVoice>
                            <nationality>gw</nationality>
                            <nationality>nz</nationality>
                            <nationality>ne</nationality>
                            <contributedTo>
                                <titleOfCollectiveWorkOrWorkPerformed>Dit is de titel van een @collectief werk</titleOfCollectiveWorkOrWorkPerformed>
                                <identifier>
                                    <identifierType>ISSN</identifierType>
                                    <identifierValue>0165-4683</identifierValue>
                                </identifier>
                            </contributedTo>
                            <resource>
                                <creationClass>
                                    <domain>literature </domain>
                                    <formOfPublication>book </formOfPublication>
                                    <pietjePuk>fi<p>lm</p></pietjePuk>
                                </creationClass>
                                <creationRole>aut</creationRole>
                                <fieldOfCreation>
                                    <fieldType>dewey</fieldType>
                                    <fieldOfCreationValue>aap</fieldOfCreationValue>
                                </fieldOfCreation>
                                <fieldOfCreation>
                                    <fieldType>dewey</fieldType>
                                    <fieldOfCreationValue>noot</fieldOfCreationValue>
                                </fieldOfCreation>
                                <fieldOfCreation>
                                    <fieldType>dewey</fieldType>
                                    <fieldOfCreationValue>mies</fieldOfCreationValue>
                                </fieldOfCreation>
                                <fieldOfCreation>
                                    <fieldOfCreationValue>Org</fieldOfCreationValue>
                                </fieldOfCreation>
                                <titleOfWork>
                                    <title>Industrielles Bauen: Leitfaden f??MU-Gesch?sf??r</title>
                                    <imprint>
                                        <publisher>vdf Hochschulverlag AG, ETH Z??h</publisher>
                                        <date>2002</date>
                                    </imprint>
                                    <identifier>
                                        <identifierValue>9789062334889</identifierValue>
                                        <identifierType>ISBN</identifierType>
                                    </identifier>
                                </titleOfWork>
                            </resource>
                            <resource>
                                <creationClass />
                                <creationRole>aut</creationRole>
                                <titleOfWork>
                                    <title>Immobilienwirtschaft akutell Beitr? zur Immobilienwirtschaftlichen Forschung 2008</title>
                                    <imprint>
                                        <publisher>vdf Hochschulverlag, Z??h</publisher>
                                        <date>2008</date>
                                    </imprint>
                                    <identifier>
                                        <identifierValue>1079537</identifierValue>
                                        <identifierType>OCN</identifierType>
                                    </identifier>
                                </titleOfWork>
                            </resource>
                            <resource>
                                <creationClass />
                                <creationRole>aut</creationRole>
                                <titleOfWork>
                                    <title>Institutional Investment Realestate Magazin</title>
                                    <imprint>
                                        <publisher>Indtitutional Investment Publishing</publisher>
                                        <date>2008</date>
                                    </imprint>
                                    <identifier>
                                        <identifierValue>907</identifierValue>
                                        <identifierType>ISWC</identifierType>
                                    </identifier>
                                </titleOfWork>
                            </resource>
                        </personOrFiction>
                    </identity>
                    <dataConfidence>false</dataConfidence>
                    <languageOfIdentity>dut</languageOfIdentity>
                    <countriesAssociated>
                        <countryCode>US</countryCode>
                        <regionOrState>OH</regionOrState>
                        <city>Detroit</city>
                    </countriesAssociated>
                    <externalInformation>
                        <source>bron</source>
                        <information>Sleutel onder de steen naast de achterdeur</information>
                        <URI>http://www.pipo.uk</URI>
                    </externalInformation>
                    <note>Dit is een notitie</note>
                </identityInformation>
                <isNot>
                    <noISNI>
                        <PPN>123397340</PPN>
                        <personalName>
                            <script>Egyp</script>
                            <nameUse>fictional</nameUse>
                            <languageOfName>dut</languageOfName>
                            <forename>Hugo, de</forename>
                            <surname>Groot</surname>
                            <numeration>II</numeration>
                            <nameTitle>Hr</nameTitle>
                        </personalName>
                    </noISNI>
                </isNot>
                <isRelated identityType="organisation">
                    <relationType>isMemberOf</relationType>
                    <noISNI>
                        <PPN>123750458</PPN>
                        <organisationName>
                            <mainName>OCLC</mainName>
                            <subdivisionName>PADO</subdivisionName>
                            <subdivisionName>Pica</subdivisionName>
                            <subdivisionName>FLIP</subdivisionName>
                        </organisationName>
                    </noISNI>
                    <relationQualification>hot</relationQualification>
                    <startDateOfRelationship>1998-08-15</startDateOfRelationship>
                    <endDateOfRelationship>2003-02-14</endDateOfRelationship>
                </isRelated>
            </Request>
        '''
        headers = {'content-type': 'application/atom+xml'}
        response = requests.post(url, data=payload, headers=headers, verify=False)
        assert_that(response.status_code, equal_to(requests.codes.ok), 'response code')

    def testCommunicateWithTheISNIAtomPubAPIUsingAMinimalRequest(self):
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

    def testCommunicateWithTheISNIAtomPubAPIUsingAnInvalidRequest(self):
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
        assert_that(response.status_code, equal_to(requests.codes.not_acceptable), 'response code')

    def testAssignAnISNIUsingAValidMinimalRequest(self):
        registry = NameRegistry(assignHost='isni-m-acc.oclc.nl')
        isni = registry.assign(u"Jan", u"Baerthel", u"Industrielles Bauen: Leitfaden", u"Industrielles Bauen")

        assert_that(isni, equal_to('0000000124568061'))