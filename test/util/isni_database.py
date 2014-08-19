# -*- coding: utf-8 -*-

from flask import Flask, request
from threading import Thread
import requests
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)

port = 5000
database = {}


def format_name(forename, surname):
    return u"""\
            <personalName>
              <forename>{forename}</forename>
              <surname>{surname}</surname>
            </personalName>\
""".format(forename=forename, surname=surname)


def format_record(number, isni, names):
    return u"""\
    <srw:record>
    <srw:recordSchema>isni-b</srw:recordSchema>
    <srw:recordPacking>xml</srw:recordPacking>
    <srw:recordData>
    <responseRecord>
      <ISNIAssigned>
        <isniUnformatted>{isni}</isniUnformatted>
        <isniURI>http://isni.org/isni/{isni}</isniURI>
        <dataConfidence>30</dataConfidence>
        <ISNIMetadata>
          <identity>
          <personOrFiction>
{names}
          </personOrFiction>
          </identity>
        </ISNIMetadata>
      </ISNIAssigned>
    </responseRecord>
    </srw:recordData>
    <srw:recordPosition>{number}</srw:recordPosition>
    </srw:record>\
""".format(number=number, isni=isni, names='\n'.join([format_name(forename, surname) for forename, surname in names]))


def format_results(identities):
    return u"""\
<srw:searchRetrieveResponse \
xmlns:srw="http://www.loc.gov/zing/srw/" \
xmlns:dc="http://purl.org/dc/elements/1.1/" \
xmlns:diag="http://www.loc.gov/zing/srw/diagnostic/" \
xmlns:xcql="http://www.loc.gov/zing/cql/xcql/">
  <srw:version>1.1</srw:version>
  <srw:numberOfRecords>{count}</srw:numberOfRecords>
  <srw:resultSetId>SIDf1dbf3c0-5S9</srw:resultSetId>
  <srw:records>
{records}
  </srw:records>
</srw:searchRetrieveResponse>
""".format(count=len(database),
           records='\n'.join([format_record(index + 1, isni, identities[isni]) for index, isni in enumerate(identities)]))


def identities_matching(keywords):
    matching_identities = {}
    for isni, full_names in database.iteritems():
        all_names = [name for full_name in full_names for name in full_name]

        def matches(keyword, names):
            return reduce(lambda match, name: match or keyword.lower() in name.lower(), names, False)

        def hit(terms, names):
            reduce(lambda match, term: match and matches(term, names), terms, True)

        if hit(keywords, all_names):
            matching_identities[isni] = full_names

    return matching_identities


@app.route("/sru")
def lookup():
    search_query = request.args['query']
    if not search_query and search_query.startswith('pica.nw='):
        return format_results([])

    def unquote(s):
        return s[1:-1]

    search_term = unquote(search_query.split('=')[1])
    keywords = search_term.split('+')
    return format_results(identities_matching(keywords))


@app.route("/shutdown")
def shutdown():
    handler = request.environ.get('werkzeug.server.shutdown')
    if handler is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    handler()


def run():
    app.run(port=port)

server = Thread(target=run)


def start():
    server.start()


def stop():
    requests.get("http://localhost:{port}/shutdown".format(port=port))
    server.join()