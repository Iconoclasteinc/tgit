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

import requests
from lxml import etree


class NameRegistry(object):
    namespaces = {
        'srw': 'http://www.loc.gov/zing/srw/'
    }

    def __init__(self, host, port=None, secure=False, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.secure = secure

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

    def formatKeywords(self, keywords):
        formattedKeywords = [keyword + '*' for keyword in keywords]
        formattedKeywords[0] += ','
        return formattedKeywords

    def payload(self, keywords):
        searchTerms = '+'.join(self.formatKeywords(keywords))
        return '?query=pica.nw%%3D"%(searchTerms)s"' \
               '&operation=searchRetrieve' \
               '&recordSchema=isni-e' \
               '&maximumRecords=20' % locals()

    def extractRecords(self, results):
        for record in results.xpath('//responseRecord'):
            identity = self.parseIdentity(record)
            if identity is None:
                continue
            yield identity

    def extractNumberOfRecords(self, results):
        return results.xpath('//srw:numberOfRecords/text()', namespaces=self.namespaces)[0]

    def searchByKeywords(self, *keywords):
        response = requests.get(self.uri() + self.payload(keywords), verify=False)
        results = etree.fromstring(response.content)
        matches = self.extractRecords(results)
        numberOfRecords = self.extractNumberOfRecords(results)
        return numberOfRecords, matches

    def parseIdentity(self, record):
        assigned = record.find('ISNIAssigned')
        if assigned is not None:
            isni = assigned.find("isniUnformatted").text
            surnames = [s.text for s in assigned.xpath('.//personalName/surname')]
            forenames = [f.text for f in assigned.xpath('.//personalName/forename')]
            return isni, (max(forenames, key=len), max(surnames, key=len))
        return None