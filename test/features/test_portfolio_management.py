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

def test_closing_an_album(app, recordings):
    app.new_album(of_type="mp3", filename="album1")

    track = recordings.add_mp3(release_name="ignore", lead_performer="ignore", track_title="???")
    app.add_tracks_to_album(track)
    app.shows_track_list(["???"])
    app.close_album()

    app.new_album(of_type="mp3", filename="album2")
    app.shows_track_list()


def test_loading_an_album(app):
    app.new_album(of_type="mp3", filename="new_album")

    app.shows_album_metadata()
    app.change_album_metadata(release_name="Honeycomb")
    app.save()
    app.close_album()

    app.load_album("new_album.tgit")
    app.shows_album_metadata(release_name="Honeycomb")
