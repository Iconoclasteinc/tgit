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
    app.new_project("album1", of_type="mp3")

    track = recordings.add_mp3(release_name="ignore", lead_performer="ignore", track_title="???")
    app.add_tracks_to_project(track)
    app.shows_track_list(["???"])
    app.close_project()

    app.new_project("album2", of_type="mp3")
    app.shows_track_list()


def test_saving_and_loading_an_album(app, recordings):
    app.new_project("Honeycomb")

    tracks = (recordings.add_mp3(track_title="Chevere!", lead_performer="???"),
              recordings.add_mp3(track_title="Zumbar", lead_performer="???"),
              recordings.add_mp3(track_title="Salsa Coltrane", lead_performer="???"))

    app.add_tracks_to_project(*tracks)
    app.shows_project_metadata()
    app.change_project_metadata(release_name="Honeycomb")
    app.save()
    app.close_project()

    app.load_project("Honeycomb")

    app.shows_track_list(("Chevere!",), ("Zumbar",), ("Salsa Coltrane",))
    app.shows_project_metadata(release_name="Honeycomb")
    app.shows_next_track_metadata(track_title="Chevere!")
    app.shows_next_track_metadata(track_title="Zumbar")
    app.shows_next_track_metadata(track_title="Salsa Coltrane")


def test_importing_an_album_from_an_existing_track(app, recordings):
    track = recordings.add_mp3(release_name="Honeycomb", lead_performer="Joel Miller", track_title="Rashers")

    app.import_project("Honeycomb", from_track=track, of_type="mp3")

    app.shows_project_metadata(release_name="Honeycomb", lead_performer="Joel Miller")
    app.shows_next_track_metadata(track_title="Rashers")

