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
        INVALID_FORMAT = "INVALID_FORMAT"
        INVALID_DATA = "INVALID_DATA"
        SPARSE = "SPARSE"
        SUCCESS = "SUCCESS"

    def __init__(self, host=None, assign_host=None, port=None, secure=False, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.secure = secure
        self.assign_host = assign_host

    def search_by_keywords(self, *keywords):
        response = requests.get(self.uri() + create_payload_from(keywords), verify=False)
        results = etree.fromstring(response.content)
        matches = extract_response_records_from(results)
        number_of_records = extract_number_of_records(results)
        return number_of_records, matches

    def assign(self, forename, surname, title_of_works):
        response = self.request_assignation(forename, surname, title_of_works)
        return self.handle_assignation_response(etree.fromstring(response.content))

    def request_assignation(self, forename, surname, title_of_works):
        titles = "".join("<title>{0}</title>".format(title) for title in title_of_works)
        payload = create_assignation_payload(forename, surname, titles)
        headers = {"content-type": "application/atom+xml"}
        response = requests.post(self.assign_uri(), data=payload, headers=headers, verify=False)
        return response

    def handle_assignation_response(self, response):
        assigned = response.find("ISNIAssigned")
        if assigned is not None:
            return self.Codes.SUCCESS, assigned.find("isniUnformatted").text

        no_isni = response.find("noISNI")
        if no_isni is not None:
            reason = no_isni.xpath("//reason/text()")[0]
            if reason == "sparse":
                return self.Codes.SPARSE, get_information_field_value(no_isni)

            if reason == "invalid data":
                return self.Codes.INVALID_DATA, get_information_field_value(no_isni)

            if reason == "invalidFormat":
                return self.Codes.INVALID_FORMAT, get_information_field_value(no_isni)

        return None

    def uri(self):
        fragments = ["https" if self.secure else "http", "://", self.host]
        if self.port is not None:
            fragments.append(":")
            fragments.append(str(self.port))

        fragments.append("/sru")

        if self.username is not None:
            fragments.append("/username=")
            fragments.append(self.username)
            fragments.append("/password=")
            fragments.append(self.password)
            fragments.append("/DB=1.3")
        else:
            fragments.append("/DB=1.2")
        return "".join(fragments)

    def assign_uri(self):
        fragments = ["https" if self.secure else "http", "://", self.assign_host]
        if self.port is not None:
            fragments.append(":")
            fragments.append(str(self.port))

        fragments.append("/ATOM/isni")
        return "".join(fragments)


def get_information_field_value(no_isni):
    return no_isni.xpath("//information/text()")[0]


def extract_number_of_records(results):
    return results.xpath("//srw:numberOfRecords/text()", namespaces=NAMESPACES)[0]


def extract_response_records_from(results):
    matched = []
    for record in results.xpath("//responseRecord"):
        identity = parse_identity_from(record)
        if identity is not None:
            matched.append(identity)
    return matched


def parse_identity_from(record):
    assigned = record.find("ISNIAssigned")
    if assigned is not None:
        isni = assigned.find("isniUnformatted").text
        if is_person(assigned):
            surname = get_longest_in(assigned, ".//personalName/surname")
            forename = get_longest_in(assigned, ".//personalName/forename")
            date = get_longest_in(assigned, ".//personalName/dates")
            title = get_longest_in(assigned, ".//creativeActivity/titleOfWork/title")
            return isni, ("{0} {1}".format(forename, surname), date, remove_line_start_character(title))

        if is_organisation(assigned):
            name = get_organisation_name_from(assigned)
            title = get_longest_in(assigned, ".//creativeActivity/titleOfWork/title")
            return isni, (name, "", remove_line_start_character(title))

    return None


def get_organisation_name_from(record):
    organisation_names = record.xpath(".//organisation/organisationName/mainName")
    return max([normalize(name.text) for name in organisation_names], key=len) if len(organisation_names) > 0 else ""


def create_payload_from(keywords):
    return "?query=pica.nw%3D{0}+pica.st%3DA" \
           "&operation=searchRetrieve" \
           "&recordSchema=isni-e" \
           "&maximumRecords=20".format("+".join(format_keywords(keywords)))


def create_assignation_payload(forename, surname, titles):
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


def format_keywords(keywords):
    formatted_keywords = [keyword + "*" for keyword in keywords]
    formatted_keywords[0] += ","
    return formatted_keywords


def remove_line_start_character(title):
    index_of_line_start_character = title.rfind("@")
    if index_of_line_start_character > -1:
        return "".join([title[:index_of_line_start_character], title[index_of_line_start_character + 1:]])
    else:
        return title


def get_longest_in(record, xpath):
    expressions = [s.text for s in record.xpath(xpath) if s.text is not None]
    return max(expressions, key=len) if len(expressions) > 0 else ""


def is_person(record):
    return len(record.xpath(".//personalName")) > 0


def is_organisation(record):
    return len(record.xpath(".//organisation")) > 0


def normalize(name):
    index = name.find("(")
    return name if index == -1 else name[:index].strip()