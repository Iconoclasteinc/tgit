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

from test.util import isni_database


@pytest.fixture(autouse=True)
def isni(request):
    database_thread = isni_database.start()
    request.addfinalizer(lambda: isni_database.stop(database_thread))


def test_assigning_an_isni_to_the_lead_performer(app, recordings, workspace):
    tracks = [recordings.add_mp3(track_title="Salsa Coltrane", release_name="Honeycomb", lead_performer="Joel Miller")]
    isni_database.assignation_generator = iter(["0000000121707484"])

    app.import_album(*tracks)
    app.shows_album_content(["Salsa Coltrane"])
    app.shows_album_metadata(release_name="Honeycomb", lead_performer="Joel Miller")
    app.assign_isni_to_lead_performer()

    app.tag()
    workspace.contains_track(filename="Joel Miller - 01 - Salsa Coltrane.mp3",
                             release_name="Honeycomb",
                             isni="0000000121707484",
                             lead_performer="Joel Miller",
                             track_title="Salsa Coltrane")


def test_failing_to_assign_isni_to_lead_performer_when_data_is_invalid(app, recordings):
    tracks = [recordings.add_mp3(track_title="Salsa Coltrane", release_name="Honeycomb", lead_performer="Joel Miller")]
    isni_database.assignation_generator = iter(["invalid data"])

    app.import_album(*tracks)
    app.shows_album_content(["Salsa Coltrane"])
    app.shows_album_metadata(release_name="Honeycomb", lead_performer="Joel Miller")
    app.fails_to_assign_isni_to_lead_performer()
