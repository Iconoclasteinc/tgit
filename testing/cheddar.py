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
import json
import logging
import time
from functools import wraps
from threading import Thread

import requests
from flask import Flask, request, Response

from cute import platforms

FLASK_STARTUP_DELAY = 0 if platforms.windows else 0.01

logging.getLogger("werkzeug").setLevel(logging.ERROR)
token_queue = iter([])
response_code_queue = []
allowed_bearer_token = ""
identities_for_lookup = {}
identities_for_assignation = {}

_app = Flask(__name__)


def port():
    return 5001


def host():
    return "127.0.0.1"


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
    if len(response_code_queue):
        return Response(status=response_code_queue.pop(0))

    phrase = request.args.get("q")

    identities_to_return = []
    if phrase in identities_for_lookup:
        identities_to_return.extend(identities_for_lookup[phrase])

    response = Response(status=200)
    response.set_data(json.dumps(identities_to_return))
    response.headers.add_header("X-Total-Count", len(identities_to_return))
    return response


@_app.route("/api/identities", methods=["POST"])
@_requires_bearer_token
def _assign():
    if len(response_code_queue):
        return Response(status=response_code_queue.pop(0))

    name = json.loads(request.data.decode())["name"]

    if name in identities_for_assignation:
        return json.dumps(identities_for_assignation[name])

    return json.dumps({})


@_app.route("/api/authentications", methods=["POST"])
@_requires_auth
def _authenticate():
    token = next(token_queue)
    return json.dumps({"token": token, "permissions": ["isni.lookup", "isni.assign"]})


@_app.route("/shutdown")
def _shutdown():
    handler = request.environ.get("werkzeug.server.shutdown")
    if handler is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    handler()
    return "Server shutting down..."


def start():
    global token_queue, response_code_queue, allowed_bearer_token, identities_for_lookup, identities_for_assignation
    token_queue = iter([])
    response_code_queue = []
    allowed_bearer_token = ""
    identities_for_lookup = {}
    identities_for_assignation = {}

    server_thread = Thread(target=lambda: _app.run(port=port()))
    server_thread.start()
    time.sleep(FLASK_STARTUP_DELAY)
    return server_thread


def stop(server_thread):
    requests.get("http://{host}:{port}/shutdown".format(host=host(), port=port()))
    server_thread.join()
