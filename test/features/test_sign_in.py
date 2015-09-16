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
import pytest
import requests


@pytest.yield_fixture()
def name_server():
    from test.util import isni_database
    database_thread = isni_database.start()
    yield isni_database
    isni_database.stop(database_thread)


@pytest.yield_fixture()
def platform(name_server):
    from test.util.platform import isni_api
    server_thread = isni_api.start(name_server.host(), name_server.port())
    yield isni_api
    isni_api.stop(server_thread)


@pytest.mark.wip
def test_signing_in_enables_isni_lookup(app, platform):
    platform.token_queue = iter(["token12345"])
    app.sign_in()
    app.new_album()
    app.registered_features_enabled()


@pytest.mark.wip
def test_basic_auth(platform):
    platform.token_queue = iter(["token12345"])
    response = requests.post("http://localhost:5001/api/authentications", auth=('jonathan', 'passw0rd'))
    token = response.content
