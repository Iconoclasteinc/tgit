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

__all__ = ["NameRegistry"]

NAMESPACES = {
    "srw": "http://www.loc.gov/zing/srw/"
}


class NameRegistry(object):
    class Codes(object):
        ERROR = "ERROR"
        SUCCESS = "SUCCESS"

    def __init__(self, host, port=None, secure=False):
        self._host = host
        self._port = port
        self._secure = secure

    def search_by_keywords(self, *keywords):
        response = requests.get(self._lookup_uri(*keywords), verify=False)
        results = etree.fromstring(response.content)
        matches = _extract_response_records_from(results)
        number_of_records = _extract_number_of_records(results)
        return number_of_records, matches

    def assign(self, forename, surname, title_of_works):
        response = self._request_assignation(forename, surname, title_of_works)
        return self._handle_assignation_response(etree.fromstring(response.content))

    def _request_assignation(self, forename, surname, title_of_works):
        payload = _create_assignation_payload(forename, surname, title_of_works)
        headers = {"content-type": "application/atom+xml"}
        response = requests.post(self._assignation_uri(), data=payload, headers=headers, verify=False)
        return response

    def _handle_assignation_response(self, response):
        assigned = response.find("ISNIAssigned")
        if assigned is not None:
            return self.Codes.SUCCESS, assigned.find("isniUnformatted").text

        no_isni = response.find("noISNI")
        if no_isni is not None:
            return self.Codes.ERROR, _get_information_field_value(no_isni)

        return None

    def _lookup_uri(self, *keywords):
        return self._hostname + "/isni/lookup" + _create_payload_from(keywords)

    def _assignation_uri(self):
        return self._hostname + "/isni/assign"

    @property
    def _hostname(self):
        fragments = ["https" if self._secure else "http", "://", self._host]
        if self._port is not None:
            fragments.append(":")
            fragments.append(str(self._port))

        return "".join(fragments)


def _get_information_field_value(no_isni):
    return no_isni.xpath("//information/text()")[0]


def _extract_number_of_records(results):
    return results.xpath("//srw:numberOfRecords/text()", namespaces=NAMESPACES)[0]


def _extract_response_records_from(results):
    matched = []
    for record in results.xpath("//responseRecord"):
        identity = _parse_identity_from(record)
        if identity is not None:
            matched.append(identity)
    return matched


def _parse_identity_from(record):
    assigned = record.find("ISNIAssigned")
    if assigned is not None:
        isni = assigned.find("isniUnformatted").text
        if _is_person(assigned):
            surname = _get_longest_in(assigned, ".//personalName/surname")
            forename = _get_longest_in(assigned, ".//personalName/forename")
            date = _get_longest_in(assigned, ".//personalName/dates")
            title = _get_longest_in(assigned, ".//creativeActivity/titleOfWork/title")
            return isni, ("{0} {1}".format(forename, surname), date, _remove_line_start_character(title))

        if _is_organisation(assigned):
            name = _get_organisation_name_from(assigned)
            title = _get_longest_in(assigned, ".//creativeActivity/titleOfWork/title")
            return isni, (name, "", _remove_line_start_character(title))

    return None


def _get_organisation_name_from(record):
    organisation_names = record.xpath(".//organisation/organisationName/mainName")
    return max([_normalize(name.text) for name in organisation_names], key=len) if len(organisation_names) > 0 else ""


def _create_payload_from(keywords):
    return "?query=pica.nw%3D{0}+pica.st%3DA" \
           "&operation=searchRetrieve" \
           "&recordSchema=isni-e" \
           "&maximumRecords=20".format("+".join(_format_keywords(keywords)))


def _create_assignation_payload(forename, surname, title_of_works):
    titles = "".join("<title>{0}</title>".format(title) for title in title_of_works)

    return """
        <Request>
            <requestID>
                <dateTimeOfRequest>{0}</dateTimeOfRequest>
                <requestorTransactionId></requestorTransactionId>
            </requestID>
            <identityInformation>
                <requestorIdentifierOfIdentity>
                    <referenceURI>{1}</referenceURI>
                    <identifier>0123456789</identifier>
                </requestorIdentifierOfIdentity>
                <identity>
                    <personOrFiction>
                        <personalName>
                            <nameUse>public and private</nameUse>
                            <surname>{2}</surname>
                            <forename>{3}</forename>
                        </personalName>
                        <resource>
                            <creationClass>
                                <domain>literature</domain>
                                <formOfPublication>book</formOfPublication>
                                <pietjePuk>fi<p>lm</p></pietjePuk>
                            </creationClass>
                            <creationRole>{4}</creationRole>
                            <titleOfWork>
                                {5}
                            </titleOfWork>
                        </resource>
                    </personOrFiction>
                </identity>
            </identityInformation>
        </Request>
    """.format(datetime.utcnow(), "http://tagtamusique.com/", surname, forename, "prf", titles)


def _format_keywords(keywords):
    formatted_keywords = [keyword + "*" for keyword in keywords]
    formatted_keywords[0] += ","
    return formatted_keywords


def _remove_line_start_character(title):
    index_of_line_start_character = title.rfind("@")
    if index_of_line_start_character > -1:
        return "".join([title[:index_of_line_start_character], title[index_of_line_start_character + 1:]])
    else:
        return title


def _get_longest_in(record, xpath):
    expressions = [s.text for s in record.xpath(xpath) if s.text is not None]
    return max(expressions, key=len) if len(expressions) > 0 else ""


def _is_person(record):
    return len(record.xpath(".//personalName")) > 0


def _is_organisation(record):
    return len(record.xpath(".//organisation")) > 0


def _normalize(name):
    index = name.find("(")
    return name if index == -1 else name[:index].strip()
