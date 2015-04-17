# -*- coding: utf-8 -*-
#
# TGiT, Music Tagger for Professionals
# Copyright (C) 2013 Iconoclaste Musique Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
from lxml import etree
import unittest
from hamcrest import assert_that, equal_to, not_none
import requests


@unittest.skip('Exploration test')
class IsniExplorationTest(unittest.TestCase):
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
        no_isni = results.find('noISNI')
        assert_that(no_isni, not_none(), 'no ISNI tag')

        sparse = no_isni.find('reason')
        assert_that(sparse.text, equal_to('invalidFormat'), 'invalid response')

    def testAssignOrganisationWithTheISNIAtomPubAPIUsingASparseRequest(self):
        url = 'https://isni-m-acc.oclc.nl/ATOM/isni'
        payload = '''
        <Request xsi:noNamespaceSchemaLocation="ISNI%20request.xsd"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
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
        no_isni = results.find('noISNI')
        assert_that(no_isni, not_none(), 'no ISNI tag')

        sparse = no_isni.find('reason')
        assert_that(sparse.text, equal_to('sparse'), 'sparse response')

    def testAssignPersonWithTheISNIAtomPubAPIUsingASparseRequest(self):
        url = 'https://isni-m-acc.oclc.nl/ATOM/isni'
        payload = '''
            <Request xsi:noNamespaceSchemaLocation="ISNI%20request.xsd"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
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
        no_isni = results.find('noISNI')
        assert_that(no_isni, not_none(), 'no ISNI tag')

        sparse = no_isni.find('reason')
        assert_that(sparse.text, equal_to('sparse'), 'sparse response')

    def testAssignPersonWithTheISNIAtomPubAPIUsingAPossibleMatchesRequestReturningScoreOf06(self):
        url = 'https://isni-m-acc.oclc.nl/ATOM/isni'
        payload = '''
            <Request xsi:noNamespaceSchemaLocation="ISNI%20request.xsd"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
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
        no_isni = results.find('noISNI')
        assert_that(no_isni, not_none(), 'no ISNI tag')

        sparse = no_isni.find('reason')
        assert_that(sparse.text, equal_to('possibleMatch'), 'possible matches response')

    def testAssignPersonWithTheISNIAtomPubAPIUsingAPossibleMatchesRequestReturningScoreOf085(self):
        url = 'https://isni-m-acc.oclc.nl/ATOM/isni'
        payload = '''
            <Request xsi:noNamespaceSchemaLocation="ISNI%20request.xsd"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
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
                    <note>
                        trying to get low score matches with 121312917, 025525212, 038373734, 036219002, 114367671, 107884143
                    </note>
                </identityInformation>
            </Request>
        '''
        headers = {'content-type': 'application/atom+xml'}
        response = requests.post(url, data=payload, headers=headers, verify=False)
        assert_that(response.status_code, equal_to(requests.codes.ok), 'response code')

        content = response.content
        results = etree.fromstring(content)
        no_isni = results.find('noISNI')
        assert_that(no_isni, not_none(), 'no ISNI tag')

        sparse = no_isni.find('reason')
        assert_that(sparse.text, equal_to('possibleMatch'), 'possible matches response')