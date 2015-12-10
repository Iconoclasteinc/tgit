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


def test_assigning_an_isni_to_the_lead_performer(app, recordings, workspace, platform):
    track = recordings.add_mp3(track_title="Salsa Coltrane", release_name="Honeycomb", lead_performer="Joel Miller")
    platform.token_queue = iter(["TheSuperToken"])
    platform.allowed_bearer_token = "TheSuperToken"
    platform.identities["Joel Miller"] = {
        "id": "0000000121707484",
        "type": "individual",
        "firstName": "Joel",
        "lastName": "Miller",
        "works": [
            {"title": "Honeycombs"}
        ]
    }

    app.sign_in()
    app.import_album("Honeycomb", from_track=track)
    app.shows_track_list(["Salsa Coltrane"])
    app.shows_album_metadata(release_name="Honeycomb", lead_performer="Joel Miller")
    app.assign_isni_to_lead_performer()

    app.save_album()
    workspace.contains_track(album="Honeycomb",
                             filename="Joel Miller - 01 - Salsa Coltrane.mp3",
                             release_name="Honeycomb",
                             lead_performer=("Joel Miller", "0000000121707484"),
                             track_title="Salsa Coltrane")
