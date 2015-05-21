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
from hamcrest import assert_that, equal_to, not_none, contains_string
import pytest
import requests


@pytest.fixture()
def url():
    return "https://isni-m-acc.oclc.nl/ATOM/isni"


@pytest.fixture()
def headers():
    return {"content-type": "application/atom+xml"}


def request_has_not_assigned_an_isni(response):
    results = etree.fromstring(response.content)
    no_isni = results.find("noISNI")
    assert_that(no_isni, not_none(), "no ISNI tag")


def request_has_assigned_an_isni(response):
    results = etree.fromstring(response.content)
    assert_that(results.find("ISNIAssigned"), not_none(), "response code")


def request_was_ok(response):
    assert_that(response.status_code, equal_to(requests.codes.ok), "response code")


def request_was_not_acceptable(response):
    assert_that(response.status_code, equal_to(requests.codes.not_acceptable), "response code")


def response_has_invalid_data_reason(response):
    results = etree.fromstring(response.content)
    no_isni = results.find("noISNI")
    assert_that(no_isni.find("reason").text, equal_to("invalid data"), "invalid response")
    return no_isni


def request_had_incomplete_data(response):
    no_isni = response_has_invalid_data_reason(response)
    information = no_isni.find("information")
    assert_that(information.text.lower(), contains_string("tag 028c is missing"), "missing information")


def request_was_malformed(response):
    no_isni = response_has_invalid_data_reason(response)
    information = no_isni.find("information")
    assert_that(information.text.lower(), contains_string("tag 028c is missing"), "missing information")


def request_contained_sparse_information(response):
    no_isni = response_has_invalid_data_reason(response)
    information = no_isni.find("information")
    assert_that(information.text.lower(), contains_string("sparse"), "sparse information")


def request_has_possible_matches(response):
    no_isni = response_has_invalid_data_reason(response)
    sparse = no_isni.find("reason")
    assert_that(sparse.text, equal_to("possibleMatch"), "possible matches response")


def request_had_insufficient_information(response):
    no_isni = response_has_invalid_data_reason(response)
    information = no_isni.find("information")
    assert_that(information.text.lower(), contains_string("insufficient distinguishing information"),
                "insufficient information")


def test_assign_isni_using_the_remote_accept_environment_with_a_well_formed_request(url, headers):
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
                        <gender>female</gender>
                        <birthDate>1953-02-13</birthDate>
                        <nationality>US</nationality>
                        <resource>
                            <creationClass>test</creationClass>
                            <creationRole>aut</creationRole>
                            <titleOfWork>
                                <title>Men and demons</title>
                                <imprint>
                                    <publisher>HarperPerennial</publisher>
                                </imprint>
                                <identifier>
                                    <identifierValue>9780060974961</identifierValue>
                                    <identifierType>ISBN</identifierType>
                                </identifier>
                            </titleOfWork>
                        </resource>
                        <contributedTo>
                            <titleOfCollectiveWorkOrWorkPerformed>
                                Amercan History Journal
                            </titleOfCollectiveWorkOrWorkPerformed>
                            <identifier>
                                <identifierType>ISSN</identifierType>
                                <identifierValue>0010-0870</identifierValue>
                            </identifier>
                        </contributedTo>
                        <personalNameVariant>
                            <nameUse>private</nameUse>
                            <surname>Williams</surname>
                            <forename>Pamela Jane</forename>
                        </personalNameVariant>
                    </personOrFiction>
                </identity>
                <languageOfIdentity>eng</languageOfIdentity>
                <countriesAssociated>
                    <countryCode>US</countryCode>
                </countriesAssociated>
                <externalInformation>
                    <information>wikipedia</information>
                    <URI>http://en.wikipedia.org/wiki/Salem_witch_trials</URI>
                </externalInformation>
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
    response = requests.post(url, data=payload, headers=headers, verify=False)

    request_was_ok(response)
    request_has_assigned_an_isni(response)


def test_assign_isni_using_the_remote_accept_environment_with_an_isnot_request(url, headers):
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
                    <identifier>11112222332324</identifier>
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
                <note>should create a new record and not match with PPNs 37444949X, 36586272X and 083863184</note>
            </identityInformation>
            <isNot identityType="personOrFiction">
                <noISNI>
                    <PPN>37444949X</PPN>
                </noISNI>
            </isNot>
            <isNot identityType="personOrFiction">
                <noISNI>
                    <PPN>083863184</PPN>
                </noISNI>
            </isNot>
        </Request>
    '''

    response = requests.post(url, data=payload, headers=headers, verify=False)

    request_was_ok(response)
    request_has_assigned_an_isni(response)


def test_assign_isni_using_the_remote_accept_environment_with_a_request_containing_insufficient_info(url, headers):
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
    response = requests.post(url, data=payload, headers=headers, verify=False)

    request_was_not_acceptable(response)
    request_has_not_assigned_an_isni(response)
    request_had_insufficient_information(response)


@pytest.mark.wip
def test_assign_isni_using_the_remote_accept_environment_with_a_malformed_request(url, headers):
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
                </identity>
            </identityInformation>
    '''
    response = requests.post(url, data=payload, headers=headers, verify=False)

    request_was_not_acceptable(response)
    request_has_not_assigned_an_isni(response)
    request_was_malformed(response)


def test_assign_isni_using_the_remote_accept_environment_with_an_incomplete_request(url, headers):
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
    response = requests.post(url, data=payload, headers=headers, verify=False)

    request_was_not_acceptable(response)
    request_has_not_assigned_an_isni(response)
    request_had_incomplete_data(response)


def test_assign_isni_to_an_organisation_using_the_remote_accept_environment_with_a_sparse_request(url, headers):
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

    response = requests.post(url, data=payload, headers=headers, verify=False)

    request_was_not_acceptable(response)
    request_has_not_assigned_an_isni(response)
    request_contained_sparse_information(response)


def test_assign_isni_to_a_person_using_the_remote_accept_environment_with_a_sparse_request(url, headers):
    payload = '''
        <Request>
            <requestID>
                <dateTimeOfRequest>2001-12-17T09:30:47Z</dateTimeOfRequest>
                <requestorTransactionId>My ID</requestorTransactionId>
            </requestID>
            <identityInformation>
                <requestorIdentifierOfIdentity>
                    <referenceURI>www.rag.address.com</referenceURI>
                    <identifier>1515161634333</identifier>
                </requestorIdentifierOfIdentity>
                <otherIdentifierOfIdentity>
                    <identifier>99667784444</identifier>
                    <type>TEST</type>
                </otherIdentifierOfIdentity>
                <identity>
                    <personOrFiction>
                        <personalName>
                            <nameUse>public and private</nameUse>
                            <surname>Williamson</surname>
                            <forename>Pamela</forename>
                        </personalName>
                    </personOrFiction>
                </identity>
            </identityInformation>
        </Request>
    '''

    response = requests.post(url, data=payload, headers=headers, verify=False)

    request_was_not_acceptable(response)
    request_has_not_assigned_an_isni(response)
    request_contained_sparse_information(response)


@pytest.mark.wip
def test_assign_isni_using_the_remote_accept_environment_with_a_possible_matches_request(url, headers):
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

    response = requests.post(url, data=payload, headers=headers, verify=False)

    request_was_not_acceptable(response)
    request_has_not_assigned_an_isni(response)
    request_has_possible_matches(response)
