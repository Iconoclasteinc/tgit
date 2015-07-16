# -*- coding: utf-8 -*-
from datetime import timedelta

from hamcrest import assert_that, is_, not_none

from test.util.builders import make_track, make_album
from tgit.ui.track_list_table_model import TrackItem, Column


def test_retrieves_values_from_track_list_item():
    item = TrackItem(make_track(album=make_album(release_name="Honeycomb"),
                                track_title="Chevere!",
                                lead_performer="Joel Miller",
                                track_number=3,
                                bitrate=192000,
                                duration=in_seconds(minutes=4, seconds=12)))

    assert_that(Column.track_number.value(item).text(), is_("3"), "track number text")
    assert_that(Column.track_title.value(item).text(), is_("Chevere!"), "track title text")
    assert_that(Column.release_name.value(item).text(), is_("Honeycomb"), "release name text")
    assert_that(Column.lead_performer.value(item).text(), is_("Joel Miller"), "lead performer text")
    assert_that(Column.bitrate.value(item).text(), is_("192 kbps"), "bitrate text")
    assert_that(Column.duration.value(item).text(), is_("04:12"), "bitrate text")


def test_displays_missing_values_as_blanks():
    item = TrackItem(make_track(album=make_album()))

    assert_that(Column.track_title.value(item).text(), is_(""), "blank track title text")
    assert_that(Column.release_name.value(item).text(), is_(""), "blank release name text")
    assert_that(Column.lead_performer.value(item).text(), is_(""), "blank lead performer text")


def test_displays_icon_when_track_is_playing(qt):
    item = TrackItem(make_track())
    item.mark_playing()

    assert_that(Column.state.value(item).icon(), not_none(), "state icon")


def in_seconds(minutes, seconds):
    return timedelta(minutes=minutes, seconds=seconds).total_seconds()
