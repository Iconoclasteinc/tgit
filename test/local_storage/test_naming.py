# -*- coding: utf-8 -*-
from hamcrest import equal_to
from hamcrest import assert_that

from test.util import builders as build
from tgit.local_storage import naming


def test_names_track_file_with_lead_performer_and_track_number_and_track_title():
    track = build.track(filename='track.mp3', track_title='title', lead_performer='artist', track_number=3)

    assert_that(naming.default_scheme(track), equal_to("artist - 03 - title.mp3"), 'name of tagged file')
