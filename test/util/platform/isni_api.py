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

logging.getLogger("werkzeug").setLevel(logging.ERROR)

_app = Flask(__name__)
_name_server_uri = ""


def port():
    return 5001


def host():
    return "localhost"


@_app.route("/isni/lookup")
def _lookup():
    response = requests.get(_name_server_uri + "/sru/DB=1.2?" + request.query_string.decode(), verify=False)
    return response.content


@_app.route("/isni/assign", methods=["POST"])
def _assign():
    headers = {"content-type": "application/atom+xml"}
    response = requests.post(_name_server_uri + "/ATOM/isni", data=request.data.decode(), headers=headers, verify=False)
    return response.content


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
