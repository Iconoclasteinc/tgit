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

@pytest.yield_fixture()
def name_server():
    from test.util import isni_database
    database_thread = isni_database.start()
    yield isni_database
    isni_database.stop(database_thread)


@pytest.fixture(autouse=True)
def platform(name_server, request):
    from test.util.platform import isni_api
    server_thread = isni_api.start(name_server.host(), name_server.port())
    request.addfinalizer(lambda: isni_api.stop(server_thread))


def test_finding_the_isni_of_the_lead_performer(app, recordings, workspace, name_server):
    track = recordings.add_mp3(track_title="Salsa Coltrane", release_name="Honeycomb", lead_performer="Joel Miller")
    name_server.persons["0000000121707484"] = [{"names": [("Joel", "Miller", "1969-")], "titles": ["Honeycombs"]}]

    app.import_album("Honeycomb", track)
    app.shows_track_list(["Salsa Coltrane"])
    app.shows_album_metadata(release_name="Honeycomb", lead_performer="Joel Miller")
    app.find_isni_of_lead_performer()

    app.save_album()
    workspace.contains_track(album="Honeycomb",
                             filename="Joel Miller - 01 - Salsa Coltrane.mp3",
                             release_name="Honeycomb",
                             isni="0000000121707484",
                             lead_performer="Joel Miller",
                             track_title="Salsa Coltrane")
