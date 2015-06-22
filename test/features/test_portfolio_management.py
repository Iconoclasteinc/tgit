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


def test_closing_and_starting_a_new_album(app, recordings):
    app.new_album(of_type="mp3", filename="album1")

    track = recordings.add_mp3(release_name="ignore", lead_performer="ignore", track_title="???")
    app.add_tracks_to_album(track)
    app.shows_album_content(["???"])
    app.close_album()

    app.new_album(of_type="mp3", filename="album2")
    app.shows_album_content()


def test_saving_and_loading_an_album(app, recordings):
    app.new_album(of_type="mp3", filename="new_album")

    tracks = (recordings.add_mp3(track_title="Chevere!", lead_performer="???"),
              recordings.add_mp3(track_title="Zumbar", lead_performer="???"),
              recordings.add_mp3(track_title="Salsa Coltrane", lead_performer="???"))

    app.add_tracks_to_album(*tracks)
    app.shows_album_metadata()
    app.change_album_metadata(release_name="Honeycomb")
    app.save()
    app.close_album()

    app.load_album("new_album.tgit")

    app.shows_album_content(("Chevere!",), ("Zumbar",), ("Salsa Coltrane",))
    app.shows_album_metadata(release_name="Honeycomb")
    app.shows_next_track_metadata(track_title="Chevere!")
    app.shows_next_track_metadata(track_title="Zumbar")
    app.shows_next_track_metadata(track_title="Salsa Coltrane")
