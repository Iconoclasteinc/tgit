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

from test.util import doubles
from test.drivers.application_runner import ApplicationRunner
from test.util import isni_database


@pytest.yield_fixture
def library(tmpdir):
    recordings = doubles.recording_library(tmpdir.strpath)
    yield recordings
    recordings.delete()


@pytest.yield_fixture
def app():
    runner = ApplicationRunner()
    runner.start()
    yield runner
    runner.stop()


@pytest.fixture(autouse=True)
def isni(request):
    database_thread = isni_database.start()
    request.addfinalizer(lambda: isni_database.stop(database_thread))


@pytest.yield_fixture()
def isni_actions():
    yield isni_database.assignation_actions
    isni_database.assignation_actions.clear()


def test_assigning_an_isni_to_the_lead_performer(app, library, isni_actions):
    tracks = [library.add_mp3(track_title="Salsa Coltrane", releaseName="Honeycomb", lead_performer="Joel Miller")]
    isni_actions.append("0000000121707484")

    app.new_album("mp3", *tracks)
    app.shows_album_content(["Salsa Coltrane"])
    app.shows_album_metadata(releaseName="Honeycomb", lead_performer="Joel Miller")
    app.assign_isni_to_lead_performer()

    library.contains("Joel Miller - 01 - Salsa Coltrane.mp3",
                     releaseName="Honeycomb",
                     isni="0000000121707484",
                     lead_performer="Joel Miller",
                     track_title="Salsa Coltrane")