# -*- coding: utf-8 -*-

import csv
from io import StringIO

import pytest
from hamcrest import assert_that, contains, has_item
from hamcrest.core.core.isequal import equal_to

from test.util import builders as build
from tgit.local_storage.csv_format import CsvFormat, to_boolean


@pytest.fixture
def formatter():
    return CsvFormat()


@pytest.fixture
def out():
    return StringIO()


def test_includes_header_row(formatter, out):
    album = build.album()
    formatter.write(album, out)

    rows = read_csv(out)
    headers = next(rows)
    assert_that(headers, contains("Release Name",
                                  "Compilation",
                                  "Lead Performer",
                                  "Lead Performer ISNI",
                                  "Lead Performer Origin",
                                  "Guest Performers",
                                  "Label Name",
                                  "Catalog Number",
                                  "UPC/EAN",
                                  "Comments",
                                  "Release Date",
                                  "Recording Date",
                                  "Recording Studio",
                                  "Recording Location",
                                  "Production Company",
                                  "Production Location",
                                  "Music Producer",
                                  "Mixer",
                                  "Primary Style",
                                  "Track Title",
                                  "Version Information",
                                  "Track Number",
                                  "Total Tracks",
                                  "Featured Guest",
                                  "Lyrics",
                                  "Language",
                                  "Publisher",
                                  "Lyricist",
                                  "Lyricist ISNI",
                                  "Composer",
                                  "ISRC",
                                  "Tags"), "header")


def test_writes_track_metadata_in_columns(formatter, out):
    album = build.album(
        release_name="Release Name",
        lead_performer=("Lead Performer", "0000123456789"),
        lead_performer_region=("CA",),
        guest_performers=[("Instrument1", "Performer1"), ("Instrument2", "Performer2")],
        label_name="Label Name",
        catalog_number="Catalog Number",
        upc="Barcode",
        comments="Comments\n...\n...",
        release_time="2014",
        recording_time="2013")

    track = build.track(
        track_title="Track Title",
        versionInfo="Version Info",
        featuredGuest="Featuring",
        lyrics="Lyrics\n...\...\n...",
        language="eng",
        publisher="Publisher",
        lyricist=("Lyricist", "9876543210000000"),
        composer="Composer",
        isrc="ISRC",
        labels="Tag1 Tag2 Tag3",
        recording_studio="Studio",
        recording_studio_region=("CA",),
        production_company="Production Company",
        production_company_region=("CA",),
        music_producer="Music Producer",
        mixer="Mixing Engineer",
        primary_style="Genre")

    album.add_track(track)
    track.track_number = 3
    track.total_tracks = 9

    formatter.write(album, out)

    rows = read_csv(out)
    _ = next(rows)
    data = next(rows)
    assert_that(data, contains("Release Name",
                               "False",
                               "Lead Performer",
                               "0000123456789",
                               "CA",
                               "Instrument1: Performer1; Instrument2: Performer2",
                               "Label Name",
                               "Catalog Number",
                               "Barcode",
                               "Comments\r...\r...",
                               "2014",
                               "2013",
                               "Studio",
                               "CA",
                               "Production Company",
                               "CA",
                               "Music Producer",
                               "Mixing Engineer",
                               "Genre",
                               "Track Title",
                               "Version Info",
                               "3",
                               "9",
                               "Featuring",
                               "Lyrics\r...\...\r...",
                               "eng",
                               "Publisher",
                               "Lyricist",
                               "9876543210000000",
                               "Composer",
                               "ISRC",
                               "Tag1 Tag2 Tag3"), "row")


def test_converts_booleans_to_text():
    assert_that(to_boolean(None), equal_to("False"), "boolean(None)")
    assert_that(to_boolean(False), equal_to("False"), "boolean(False)")
    assert_that(to_boolean(True), equal_to("True"), "boolean(True)")


def test_writes_one_record_per_track_in_album(formatter, out):
    album = build.album(tracks=[build.track(track_title="Song 1"),
                                build.track(track_title="Song 2"),
                                build.track(track_title="Song 3")])

    formatter.write(album, out)

    rows = read_csv(out)
    _ = next(rows)
    assert_that(next(rows), has_item("Song 1"), "first row")
    assert_that(next(rows), has_item("Song 2"), "second row")
    assert_that(next(rows), has_item("Song 3"), "third row")


def test_make_line_breaks_excel_friendly_by_converting_line_feeds_to_carriage_returns(formatter, out):
    album = build.album(comments="Comments\nspanning\nseveral lines", tracks=[build.track()])

    formatter.write(album, out)

    csv_file = read_csv(out)
    _ = next(csv_file)
    assert_that(next(csv_file), has_item("Comments\rspanning\rseveral lines"), "row with line feeds")


def read_csv(output_string):
    output_string.seek(0)
    return csv.reader(output_string)
