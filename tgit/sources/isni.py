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

from collections import Counter
import requests
from lxml import etree


class NameRegistry(object):
    def __init__(self, host, port=80):
        self.host = host
        self.port = port

    def uri(self):
        return "http://{host}:{port}".format(host=self.host, port=self.port)

    def searchByKeywords(self, *keywords):
        payload = {'query': u'pica.nw="{term}"'.format(term='+'.join(keywords)),
                   'operation': 'searchRetrieve',
                   'recordSchema': 'isni-b',
                   'maximumRecords': '10'}
        response = requests.get("{uri}/sru/DB=1.2".format(uri=self.uri()), params=payload)
        results = etree.fromstring(response.content)
        records = results.xpath('//responseRecord')

        matches = []
        for record in records:
            identity = self.parseIdentity(record)
            if identity:
                matches.append(identity)

        return matches

    def parseIdentity(self, record):
        assigned = record.find('ISNIAssigned')
        if assigned is not None:
            id = assigned.find("isniUnformatted").text
            surnames = [s.text for s in assigned.xpath('.//personalName/surname')]
            forenames = [f.text for f in assigned.xpath('.//personalName/forename')]
            return id, self.mostCommonOf(forenames), self.mostCommonOf(surnames)

    @staticmethod
    def mostCommonOf(terms):
        return Counter(terms).most_common(1)[0][0]