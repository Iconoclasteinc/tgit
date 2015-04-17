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


__all__ = ["port", "identities", "start", "stop"]

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)
app = Flask(__name__)
port = 5000
identities = {}


@app.route("/sru/DB=1.2")
def lookup():
    search_query = request.args["query"]
    if not search_query and search_query.startswith("pica.nw="):
        return format_results([])

    search_term = search_query[0:search_query.rfind(" ")].split("=")[1]
    keywords = search_term.split(", ")
    return format_results(identities_matching(keywords))


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


def format_name(forename, surname, dates):
    personal_name = """
        <personalName>
            <forename>%(forename)s</forename>
            <surname>%(surname)s</surname>
            <dates>%(dates)s</dates>
        </personalName>
    """ % locals()
    return personal_name


def format_title(title):
    title = """
        <titleOfWork>
            <title>%(title)s</title>
        </titleOfWork>
    """ % locals()
    return title


def format_record(number, isni, identity):
    formatted_names = "\n".join([format_name(forename, surname, dates) for forename, surname, dates in identity["names"]])
    formatted_titles = "<creativeActivity>%s</creativeActivity>" % "\n".join(
        [format_title(title) for title in identity["titles"]]
    )

    formatted_record = """
        <srw:record>
            <srw:recordSchema>isni-b</srw:recordSchema>
            <srw:recordPacking>xml</srw:recordPacking>
            <srw:recordData>
                <responseRecord>
                    <ISNIAssigned>
                        <isniUnformatted>%(isni)s</isniUnformatted>
                        <isniURI>http://isni.org/isni/{isni}</isniURI>
                        <dataConfidence>30</dataConfidence>
                        <ISNIMetadata>
                            <identity>
                                <personOrFiction>
                                    %(formatted_names)s
                                    %(formatted_titles)s
                                </personOrFiction>
                            </identity>
                        </ISNIMetadata>
                    </ISNIAssigned>
                </responseRecord>
            </srw:recordData>
            <srw:recordPosition>%(number)s</srw:recordPosition>
        </srw:record>
    """ % locals()

    return formatted_record


def format_results(identities_to_format):
    count = len(identities_to_format)
    records = "\n".join(
        [format_record(index + 1, isni, identities_to_format[isni]) for index, isni in enumerate(identities_to_format)])

    result = """
        <srw:searchRetrieveResponse xmlns:srw="http://www.loc.gov/zing/srw/"
                                    xmlns:dc="http://purl.org/dc/elements/1.1/"
                                    xmlns:diag="http://www.loc.gov/zing/srw/diagnostic/"
                                    xmlns:xcql="http://www.loc.gov/zing/cql/xcql/">
            <srw:version>1.1</srw:version>
            <srw:numberOfRecords>%(count)s</srw:numberOfRecords>
            <srw:resultSetId>SIDf1dbf3c0-5S9</srw:resultSetId>
            <srw:records>
                %(records)s
            </srw:records>
        </srw:searchRetrieveResponse>
    """ % locals()

    return result


def identities_matching(keywords):
    matching_identities = {}
    for isni, current_identities in identities.items():
        for current_identity in current_identities:
            def hit(terms, current_name):
                first_name, last_name, _ = current_name
                first_name_found = False
                last_name_found = False
                for term in terms:
                    if term.endswith("*"):
                        first_name_found = first_name_found or first_name.lower().startswith(term.lower()[:-1])
                        last_name_found = last_name_found or last_name.lower().startswith(term.lower()[:-1])
                    else:
                        first_name_found = first_name_found or (first_name.lower() == term.lower())
                        last_name_found = last_name_found or (last_name.lower() == term.lower())
                return first_name_found and last_name_found

            for name in current_identity["names"]:
                if hit(keywords, name):
                    matching_identities[isni] = current_identity

    return matching_identities


server_thread = Thread(target=run)