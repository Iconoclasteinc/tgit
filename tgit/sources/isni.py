# -*- coding: utf-8 -*-

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
        response = requests.get("{uri}/sru".format(uri=self.uri()), params=payload)
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