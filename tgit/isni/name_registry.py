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
from datetime import datetime
import requests
from lxml import etree


class NameRegistry(object):
    namespaces = {
        'srw': 'http://www.loc.gov/zing/srw/'
    }

    def __init__(self, host=None, assignHost=None, port=None, secure=False, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.secure = secure
        self.assignHost = assignHost

    def searchByKeywords(self, *keywords):
        response = requests.get(self.uri() + self.payload(keywords), verify=False)
        results = etree.fromstring(response.content)
        matches = self.extractRecords(results)
        numberOfRecords = self.extractNumberOfRecords(results)
        return numberOfRecords, matches

    def assign(self, forename, surname, *titleOfWorks):
        creationClass = 'prf'
        referenceUri = 'http://tagtamusique.com/'
        date = datetime.utcnow()
        titles = ''.join("<title>%s</title>" % title for title in titleOfWorks)
        payload = '''
            <Request>
                <requestID>
                    <dateTimeOfRequest>%(date)s</dateTimeOfRequest>
                    <requestorTransactionId></requestorTransactionId>
                </requestID>
                <identityInformation>
                    <requestorIdentifierOfIdentity>
                        <referenceURI>%(referenceUri)s</referenceURI>
                        <identifier>0123456789</identifier>
                    </requestorIdentifierOfIdentity>
                    <identity>
                        <personOrFiction>
                            <personalName>
                                <nameUse>public and private</nameUse>
                                <surname>%(surname)s</surname>
                                <forename>%(forename)s</forename>
                            </personalName>
                            <resource>
                                <creationClass>
                                    <domain>literature </domain>
                                    <formOfPublication>book </formOfPublication>
                                    <pietjePuk>fi<p>lm</p></pietjePuk>
                                </creationClass>
                                <creationRole>%(creationClass)s</creationRole>
                                <titleOfWork>
                                    %(titles)s
                                </titleOfWork>
                            </resource>
                        </personOrFiction>
                    </identity>
                </identityInformation>
            </Request>
        ''' % locals()
        headers = {'content-type': 'application/atom+xml'}
        response = requests.post(self.assignUri(), data=payload, headers=headers, verify=False)
        content = response.content
        results = etree.fromstring(content)

        assigned = results.find('ISNIAssigned')
        if assigned is not None:
            isni = assigned.find("isniUnformatted").text
            return isni
        return None

    def uri(self):
        fragments = ['https' if self.secure else 'http', '://', self.host]
        if self.port is not None:
            fragments.append(':')
            fragments.append(self.port)

        fragments.append('/sru')

        if self.username is not None:
            fragments.append('/username=')
            fragments.append(self.username)
            fragments.append('/password=')
            fragments.append(self.password)
            fragments.append('/DB=1.3')
        else:
            fragments.append('/DB=1.2')

        return ''.join(fragments)

    def assignUri(self):
        return 'https://%s/ATOM/isni' % self.assignHost

    def formatKeywords(self, keywords):
        formattedKeywords = [keyword + '*' for keyword in keywords]
        formattedKeywords[0] += ','
        return formattedKeywords

    def payload(self, keywords):
        searchTerms = '+'.join(self.formatKeywords(keywords))
        return '?query=pica.nw%%3D%(searchTerms)s+pica.st%%3DA' \
               '&operation=searchRetrieve' \
               '&recordSchema=isni-e' \
               '&maximumRecords=20' % locals()

    def extractRecords(self, results):
        matched = []
        for record in results.xpath('//responseRecord'):
            identity = self.parseIdentity(record)
            if identity is None:
                continue
            matched.append(identity)
        return matched

    def extractNumberOfRecords(self, results):
        return results.xpath('//srw:numberOfRecords/text()', namespaces=self.namespaces)[0]

    def removeLineStartCharacter(self, title):
        indexOfLineStartCharacter = title.rfind('@')
        return ''.join([title[:indexOfLineStartCharacter], title[indexOfLineStartCharacter + 1:]])

    def getLongestIn(self, record, xpath):
        expressions = [s.text for s in record.xpath(xpath)]
        if len(expressions) > 0:
            return max(expressions, key=len)
        return ''

    def parseIdentity(self, record):
        assigned = record.find('ISNIAssigned')
        if assigned is not None:
            isni = assigned.find("isniUnformatted").text
            if self.isPerson(assigned):
                surname = self.getLongestIn(assigned, './/personalName/surname')
                forename = self.getLongestIn(assigned, './/personalName/forename')
                date = self.getLongestIn(assigned, './/personalName/dates')
                title = self.getLongestIn(assigned, './/creativeActivity/titleOfWork/title')
                return isni, ('%(forename)s %(surname)s' % locals(), date, self.removeLineStartCharacter(title))

            if self.isOrganisation(assigned):
                name = self.getOrganisationName(assigned)
                title = self.getLongestIn(assigned, './/creativeActivity/titleOfWork/title')
                return isni, (name, '', self.removeLineStartCharacter(title))

        return None

    def isPerson(self, record):
        return len(record.xpath('.//personalName')) > 0

    def isOrganisation(self, record):
        return len(record.xpath('.//organisation')) > 0

    def getOrganisationName(self, record):
        organisationNames = record.xpath('.//organisation/organisationName/mainName')
        if len(organisationNames) == 0:
            return ''

        return max([self.normalizeOrganisationName(name.text) for name in organisationNames], key=len)

    def normalizeOrganisationName(self, name):
        index = name.find('(')
        return name if index == -1 else name[:index].strip()
