# -*- coding: utf-8 -*-
from PyQt5.QtCore import QSettings
import pytest

import tgit
from tgit.preferences import Preferences
from test.util import resources, doubles
from test.drivers.application_runner import ApplicationRunner


def test_ordering_tracks_in_album(app, recordings):
    app.new_album()

    tracks = (recordings.add_mp3(track_title="Zumbar"),
              recordings.add_mp3(track_title="Salsa Coltrane"),
              recordings.add_mp3(track_title="Chevere!"),
              recordings.add_mp3(track_title="Horse Power"),
              recordings.add_mp3(track_title="Big Ideas"))

    app.add_tracks_to_album(*tracks)

    app.shows_album_content(["Zumbar"], ["Salsa Coltrane"], ["Chevere!"], ["Horse Power"], ["Big Ideas"])
    app.change_order_of_tracks(["Chevere!"], ["Zumbar"], ["Salsa Coltrane"], ["Big Ideas"], ["Horse Power"])

    app.shows_album_metadata()

    app.shows_next_track_metadata(track_title="Chevere!")
    app.shows_next_track_metadata(track_title="Zumbar")
    app.shows_next_track_metadata(track_title="Salsa Coltrane")
    app.shows_next_track_metadata(track_title="Big Ideas")
    app.shows_next_track_metadata(track_title="Horse Power")


def test_removing_tracks_from_album(app, recordings):
    app.new_album()

    tracks = (recordings.add_mp3(track_title="Horse Power"),
              recordings.add_mp3(track_title="Chevere!"),
              recordings.add_mp3(track_title="Zumbar"),
              recordings.add_mp3(track_title="Big Ideas"),
              recordings.add_mp3(track_title="Salsa Coltrane"))

    app.add_tracks_to_album(*tracks)

    app.shows_album_content(["Horse Power"], ["Chevere!"], ["Zumbar"], ["Big Ideas"], ["Salsa Coltrane"])
    app.remove_track("Big Ideas")
    app.shows_album_content(["Horse Power"], ["Chevere!"], ["Zumbar"], ["Salsa Coltrane"])
    app.remove_track("Horse Power")
    app.shows_album_content(["Chevere!"], ["Zumbar"], ["Salsa Coltrane"])

    app.shows_album_metadata()

    app.shows_next_track_metadata(track_title="Chevere!")
    app.shows_next_track_metadata(track_title="Zumbar")
    app.shows_next_track_metadata(track_title="Salsa Coltrane")
