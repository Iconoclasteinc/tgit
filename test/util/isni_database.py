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

from threading import Thread
import logging

from flask import Flask, request
import requests


__all__ = ["port", "persons", "organisations", "start", "stop"]

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)
app = Flask(__name__)
port = 5000
persons = {}
organisations = {}


@app.route("/sru/DB=1.2")
def lookup():
    search_query = request.args["query"]
    if not search_query and search_query.startswith("pica.nw="):
        return format_results([])

    search_term = search_query[0:search_query.rfind(" ")].split("=")[1]
    keywords = search_term.split(", ")

    matches = identity_matching(keywords, persons)
    if len(matches) > 0:
        return format_results(matches)

    matches = identity_matching(keywords, organisations)
    if len(matches) > 0:
        return format_results(matches, True)

    return format_results({})


@app.route("/shutdown")
def shutdown():
    handler = request.environ.get("werkzeug.server.shutdown")
    if handler is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    handler()
    return "Server shutting down..."


def run():
    app.run(port=port)


def start():
    server_thread.start()


def stop():
    requests.get("http://localhost:{port}/shutdown".format(port=port))
    server_thread.join()


def format_person_name(forename, surname, dates):
    return """
        <personalName>
            <forename>{0}</forename>
            <surname>{1}</surname>
            <dates>{2}</dates>
        </personalName>
    """.format(forename, surname, dates)


def format_organisation_name(name):
    return """
        <organisationName>
            <mainName>{0}</mainName>
        </organisationName>
    """.format(name)


def format_title(title):
    return """
        <titleOfWork>
            <title>{0}</title>
        </titleOfWork>
    """.format(title)


def format_identity(identity, is_organisation):
    ident = ["<organisation>" if is_organisation else "<personOrFiction>"]
    if is_organisation:
        ident.extend([format_organisation_name(name) for name in identity["names"]])
    else:
        ident.extend([format_person_name(forename, surname, dates) for forename, surname, dates in identity["names"]])

    ident.append("<creativeActivity>")
    ident.append("\n".join([format_title(title) for title in identity["titles"]]))
    ident.append("</creativeActivity>")
    ident.append("</organisation>" if is_organisation else "</personOrFiction>")

    return "".join(ident)


def format_record(number, isni, identity, is_organisation):
    formatted_identity = format_identity(identity, is_organisation)
    return """
        <srw:record>
            <srw:recordSchema>isni-b</srw:recordSchema>
            <srw:recordPacking>xml</srw:recordPacking>
            <srw:recordData>
                <responseRecord>
                    <ISNIAssigned>
                        <isniUnformatted>{0}</isniUnformatted>
                        <isniURI>http://isni.org/isni/{0}</isniURI>
                        <dataConfidence>30</dataConfidence>
                        <ISNIMetadata>
                            <identity>
                                {1}
                            </identity>
                        </ISNIMetadata>
                    </ISNIAssigned>
                </responseRecord>
            </srw:recordData>
            <srw:recordPosition>{2}</srw:recordPosition>
        </srw:record>
    """.format(isni, formatted_identity, number)


def format_results(identities_to_format, is_organisation=False):
    count = len(identities_to_format)
    records = "\n".join(
        [format_record(index + 1, isni, identities_to_format[isni], is_organisation) for index, isni in
         enumerate(identities_to_format)])

    return """
        <srw:searchRetrieveResponse xmlns:srw="http://www.loc.gov/zing/srw/"
                                    xmlns:dc="http://purl.org/dc/elements/1.1/"
                                    xmlns:diag="http://www.loc.gov/zing/srw/diagnostic/"
                                    xmlns:xcql="http://www.loc.gov/zing/cql/xcql/">
            <srw:version>1.1</srw:version>
            <srw:numberOfRecords>{0}</srw:numberOfRecords>
            <srw:resultSetId>SIDf1dbf3c0-5S9</srw:resultSetId>
            <srw:records>
                {1}
            </srw:records>
        </srw:searchRetrieveResponse>
    """.format(count, records)


def identity_matching(keywords, identities):
    matching_identities = {}
    for isni, current_identities in identities.items():
        for current_identity in current_identities:
            for names in current_identity["names"]:
                name_fragments = []
                if isinstance(names, tuple):
                    name_fragments.append(names[0])
                    name_fragments.append(names[1])
                else:
                    name_fragments.extend(names.split(" "))

                if hit(keywords, name_fragments):
                    matching_identities[isni] = current_identity

    return matching_identities


def hit(terms, name_fragments):
    terms_found = []
    for term in terms:
        for name in name_fragments:
            normalized_name = name.lower()
            normalized_term = term.lower()
            if term.endswith("*") and normalized_name.startswith(normalized_term[:-1]):
                terms_found.append(term)
                break
            elif normalized_name == normalized_term:
                terms_found.append(term)
                break

    return len(terms_found) == len(terms)


server_thread = Thread(target=run)