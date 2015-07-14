# -*- coding: utf-8 -*-
from hamcrest import equal_to
from hamcrest import assert_that

from test.util import builders as build
from tgit.local_storage import naming
from tgit.metadata import Image


def test_names_track_file_with_lead_performer_and_track_number_and_track_title():
    track = build.track(filename="track.mp3", track_title="title", lead_performer="artist", track_number=3)

    assert_that(naming.track_scheme(track), equal_to("artist - 03 - title.mp3"), "name of track file")


def test_names_artwork_file_with_desc_and_mime_type():
    artwork = Image("image/png", b"...", Image.FRONT_COVER, "Front Cover")

    assert_that(naming.artwork_scheme(artwork), equal_to("Front Cover.png"), "name of picture file")


def test_assumes_front_cover_image_for_artwork_without_a_description():
    artwork = Image("image/png", b"...", Image.FRONT_COVER, "")

    assert_that(naming.artwork_scheme(artwork), equal_to("Front Cover.png"), "name of picture file")
