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

from collections import Counter, namedtuple
import requests
from lxml import etree


class NameRegistry(object):
    def __init__(self, host, port=None, secure=False, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.secure = secure

    def uri(self):
        uri = "{schema}://{host}".format(schema='https' if self.secure else 'http', host=self.host)
        if self.port is not None:
            uri = "{uri}:{port}".format(uri=uri, port=self.port)

        uri += "/sru"

        if self.username is not None:
            uri = "{uri}/username={username}/password={password}/DB=1.3".format(uri=uri, username=self.username,
                                                                                password=self.password)
        else:
            uri += "/DB=1.2"

        return uri

    def searchByKeywords(self, *keywords):
        formattedKeywords = [keyword + '*' for keyword in keywords]
        formattedKeywords[0] += ','

        payload = '?query=pica.nw%3D"{term}"' \
                  '&operation=searchRetrieve' \
                  '&recordSchema=isni-e' \
                  '&maximumRecords=20'.format(term='+'.join(formattedKeywords))

        response = requests.get(self.uri() + payload, verify=False)
        results = etree.fromstring(response.content)
        records = results.xpath('//responseRecord')

        matches = []
        for record in records:
            identity = self.parseIdentity(record)
            if identity:
                matches.append(identity)

        numberOfRecords = results.xpath('//srw:numberOfRecords/text()',
                                        namespaces={'srw': 'http://www.loc.gov/zing/srw/'})[0]

        return numberOfRecords, matches

    def parseIdentity(self, record):
        assigned = record.find('ISNIAssigned')
        if assigned is not None:
            id = assigned.find("isniUnformatted").text
            surnames = [s.text for s in assigned.xpath('.//personalName/surname')]
            forenames = [f.text for f in assigned.xpath('.//personalName/forename')]
            return id, (self.longestOf(forenames), self.longestOf(surnames))

    @staticmethod
    def longestOf(terms):
        longest = ''
        for term in terms:
            if len(term) > len(longest):
                longest = term

        return longest
