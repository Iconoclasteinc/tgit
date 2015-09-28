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
from functools import wraps
import json
from threading import Thread
import logging

from flask import Flask, request, Response
import requests

logging.getLogger("werkzeug").setLevel(logging.ERROR)
token_queue = iter([])
allowed_bearer_token = ""
identities = {}

_app = Flask(__name__)
_name_server_uri = ""


def port():
    return 5001


def host():
    return "localhost"


def _check_auth(username, password):
    return username == "test@example.com" and password == "passw0rd"


def _please_authenticate():
    return Response(
        "Could not verify your access level for that URL.\n"
        "You have to login with proper credentials", 401,
        {"WWW-Authenticate": "Basic realm=\"Login Required\""})


def _requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not _check_auth(auth.username, auth.password):
            return _please_authenticate()
        return f(*args, **kwargs)
    return decorated


def _check_bearer(auth):
    if not auth.startswith("Bearer"):
        return False

    if auth.split(" ")[-1] != allowed_bearer_token:
        return False

    return True


def _requires_bearer_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not ("Authorization" in request.headers):
            return _please_authenticate()

        auth = request.headers["Authorization"]
        if not _check_bearer(auth):
            return _please_authenticate()

        return f(*args, **kwargs)
    return decorated


@_app.route("/api/identities")
@_requires_bearer_token
def _lookup():
    phrase = request.args.get("q")

    identities_to_return = []
    if phrase in identities:
        identities_to_return.append(identities[phrase])

    return json.dumps(identities_to_return)


@_app.route("/isni/lookup")
def _lookup_deprecated():
    response = requests.get(_name_server_uri + "/sru/DB=1.2?" + request.query_string.decode(), verify=False)
    return response.content


@_app.route("/isni/assign", methods=["POST"])
def _assign():
    headers = {"content-type": "application/atom+xml"}
    response = requests.post(_name_server_uri + "/ATOM/isni", data=request.data.decode(), headers=headers, verify=False)
    return response.content


@_app.route("/api/authentications", methods=["POST"])
@_requires_auth
def _authenticate():
    token = next(token_queue)
    return json.dumps({"token": token})


@_app.route("/shutdown")
def _shutdown():
    handler = request.environ.get("werkzeug.server.shutdown")
    if handler is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    handler()
    return "Server shutting down..."


def start(name_server_host, name_server_port):
    global _name_server_uri
    _name_server_uri = "http://" + name_server_host + ":" + str(name_server_port)

    server_thread = Thread(target=lambda: _app.run(port=port()))
    server_thread.start()
    return server_thread


def stop(server_thread):
    requests.get("http://{host}:{port}/shutdown".format(host=host(), port=port()))
    server_thread.join()
