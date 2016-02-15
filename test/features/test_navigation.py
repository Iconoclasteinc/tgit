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


def test_navigating_through_the_album_non_linearly(app, recordings):
    app.new_project(of_type="mp3")

    tracks = (recordings.add_mp3(track_title="Chevere!", lead_performer="???"),
              recordings.add_mp3(track_title="Zumbar", lead_performer="???"),
              recordings.add_mp3(track_title="Salsa Coltrane", lead_performer="???"))

    app.add_tracks_to_project(*tracks)

    app.shows_track_metadata(track_number=3, track_title="Salsa Coltrane")
    app.shows_track_list(["Chevere!"], ["Zumbar"], ["Salsa Coltrane"])
    app.shows_track_metadata(track_number=2, track_title="Zumbar")
    app.shows_project_metadata()
    app.shows_track_metadata(track_number=1, track_title="Chevere!")
