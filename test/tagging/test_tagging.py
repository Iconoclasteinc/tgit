# -*- coding: utf-8 -*-
from datetime import datetime

from dateutil import tz
from hamcrest import has_properties, has_entries, contains, equal_to, assert_that
import pytest

import tgit
from tgit.metadata import Image
from tgit.tagging import tagging
from test.util import doubles, builders as build

NOW = datetime(2014, 3, 23, 16, 44, 33, tzinfo=tz.tzutc())


@pytest.yield_fixture
def recordings(tmpdir):
    library = doubles.recording_library(tmpdir.mkdir("library"))
    yield library
    library.delete()


def test_loads_track_from_metadata_embedded_in_file(recordings):
    track_file = recordings.add_mp3(track_title='Chaconne')
    track = tagging.load_track(track_file)
    assert_that(track, has_properties(track_title='Chaconne'))


def test_round_trips_track_and_album_metadata(recordings):
    album = build.album(release_name='Album Title', lead_performer='Album Artist',
                        images=[build.image(mime='image/jpeg', data=b'<image data>')])
    track = build.track(filename=recordings.add_mp3(), track_title='Track Title', album=album)

    tagged_file = recordings.path('tagged.mp3')
    tagging.save_track(tagged_file, track)

    track = tagging.load_track(tagged_file)
    assert_that(track.metadata, has_entries(release_name='Album Title',
                                            lead_performer='Album Artist',
                                            track_title='Track Title'), 'metadata tags')
    assert_that(track.metadata.images, contains(Image(mime='image/jpeg', data=b'<image data>')), 'attached pictures')


def test_does_not_update_track_with_album_lead_performer_when_album_is_a_compilation(recordings):
    album = build.album(lead_performer='Various Artists', compilation=True)
    track = build.track(filename=recordings.add_mp3(), lead_performer='Track Artist', album=album)

    tagged_file = recordings.path('tagged.mp3')
    tagging.save_track(tagged_file, track)

    track = tagging.load_track(tagged_file)
    assert_that(track.lead_performer, equal_to("Track Artist"), 'lead performer')


def test_adds_version_information_to_tags(recordings):
    track = build.track(filename=recordings.add_mp3(), album=build.album())

    tagged_file = recordings.path('tagged.mp3')
    tagging.save_track(tagged_file, track, at_time=NOW)

    track = tagging.load_track(tagged_file)
    assert_that(track, has_properties(tagger='TGiT',
                                      tagger_version=tgit.__version__,
                                      tagging_time="2014-03-23 16:44:33 +0000"))


def test_gracefully_handles_when_overwriting_original_recording(recordings):
    original_file = recordings.add_mp3()
    track = build.track(filename=original_file, album=build.album())

    tagging.save_track(to_file=original_file, track=track)