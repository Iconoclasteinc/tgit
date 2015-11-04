# -*- coding: utf-8 -*-

import shutil

import pytest
from hamcrest import assert_that, has_entry, has_length, contains_inanyorder, has_entries

from test.util import flac_file
from tgit.metadata import Metadata, Image
from tgit.tagging._pictures import PictureType
from tgit.tagging.flac_container import FlacContainer

DURATION = flac_file.base.duration
BITRATE = flac_file.base.bitrate

container = FlacContainer()


@pytest.yield_fixture
def flac(tmpdir):
    def maker(**tags):
        return flac_file.make(to=tmpdir.strpath, **tags).filename

    yield maker
    shutil.rmtree(tmpdir.strpath)


def test_reads_lead_performer_from_artists_field(flac):
    metadata = container.load(flac(ARTIST="Joel Miller"))
    assert_that(metadata, has_entry('lead_performer', "Joel Miller"), "metadata")


def test_reads_bitrate_from_audio_stream_information(flac):
    metadata = container.load(flac())
    assert_that(metadata, has_entry('bitrate', BITRATE), "bitrate")


def test_reads_duration_from_audio_stream_information(flac):
    metadata = container.load(flac())
    assert_that(metadata, has_entry('duration', DURATION), "duration")


def test_reads_track_title_from_title_field(flac):
    metadata = container.load(flac(TITLE="Salsa Coltrane"))
    assert_that(metadata, has_entry('track_title', "Salsa Coltrane"), "metadata")


def test_reads_release_name_from_album_field(flac):
    metadata = container.load(flac(ALBUM="Honeycomb"))
    assert_that(metadata, has_entry('release_name', "Honeycomb"), "metadata")


def test_reads_primary_style_from_genre_field(flac):
    metadata = container.load(flac(GENRE="Modern Jazz"))
    assert_that(metadata, has_entry('primary_style', "Modern Jazz"), "metadata")


def test_reads_track_isrc_from_isrc_field(flac):
    metadata = container.load(flac(ISRC="CABL31201254"))
    assert_that(metadata, has_entry('isrc', "CABL31201254"), "metadata")


def test_reads_track_iswc_from_iswc_field(flac):
    metadata = container.load(flac(ISWC="T-345246800-1"))
    assert_that(metadata, has_entry('iswc', "T-345246800-1"), "metadata")


def test_reads_recording_time_from_date_field(flac):
    metadata = container.load(flac(DATE="2011-11-02"))
    assert_that(metadata, has_entry('recording_time', "2011-11-02"), "metadata")


def test_reads_label_name_from_organization_field(flac):
    metadata = container.load(flac(ORGANIZATION="Effendi Records Inc."))
    assert_that(metadata, has_entry('label_name', "Effendi Records Inc."), "metadata")


def test_reads_attached_pictures_from_picture_field(flac):
    metadata = container.load(flac(PICTURES=(
        ('image/jpeg', PictureType.FRONT_COVER, 'Front', b'front-cover.jpg'),
        ('image/jpeg', PictureType.BACK_COVER, 'Back', b'back-cover.jpg'))))

    assert_that(metadata.images, contains_inanyorder(
        Image('image/jpeg', b'front-cover.jpg', type_=Image.FRONT_COVER, desc='Front'),
        Image('image/jpeg', b'back-cover.jpg', type_=Image.BACK_COVER, desc='Back'),
    ))


def test_reads_tagger_name_from_tagger_field(flac):
    metadata = container.load(flac(TAGGER='TGiT'))
    assert_that(metadata, has_entry('tagger', 'TGiT'), 'metadata')


def test_reads_tagger_version_from_tagger_version_field(flac):
    metadata = container.load(flac(TAGGER_VERSION='1.0'))
    assert_that(metadata, has_entry('tagger_version', '1.0'), 'metadata')


def test_reads_tagging_time_from_tagging_time_field(flac):
    metadata = container.load(flac(TAGGING_TIME='2014-03-26 18:18:55'))
    assert_that(metadata, has_entry('tagging_time', '2014-03-26 18:18:55'), 'metadata')


def test_reads_track_number_from_track_number_field(flac):
    metadata = container.load(flac(TRACKNUMBER="3"))
    assert_that(metadata, has_entry('track_number', 3), 'metadata')


def test_reads_total_tracks_from_track_total_field(flac):
    metadata = container.load(flac(TRACKTOTAL="5"))
    assert_that(metadata, has_entry('total_tracks', 5), 'metadata')


def test_reads_lead_performer_region_from_lead_performer_region_field(flac):
    metadata = container.load(flac(LEAD_PERFORMER_REGION="CA-QC"))
    assert_that(metadata, has_entry('lead_performer_region', ("CA", "QC")), 'metadata')


def test_reads_production_company_from_producer_field(flac):
    metadata = container.load(flac(PRODUCER="Effendi Records Inc."))
    assert_that(metadata, has_entry('production_company', "Effendi Records Inc."), 'metadata')


def test_reads_music_producer_from_music_producer_field(flac):
    metadata = container.load(flac(MUSIC_PRODUCER="Joel Miller & Paul Johnston"))
    assert_that(metadata, has_entry('music_producer', "Joel Miller & Paul Johnston"), 'metadata')


def test_round_trips_metadata_to_file(flac):
    metadata = Metadata()
    metadata.addImage('image/jpeg', b'honeycomb.jpg', Image.FRONT_COVER)
    metadata['release_name'] = "St-Henri"
    metadata['lead_performer'] = "Joel Miller"
    metadata['label_name'] = "Effendi Records Inc."
    metadata['primary_style'] = "Modern Jazz"
    metadata['recording_time'] = "2007-11-02"
    metadata['track_title'] = "Salsa Coltrane"
    metadata['isrc'] = "CABL31201254"
    metadata['iswc'] = "T-345246800-1"
    metadata['tagger'] = "TGiT"
    metadata['tagger_version'] = "1.0"
    metadata['tagging_time'] = "2014-03-26 18:18:55"
    metadata['track_number'] = 3
    metadata['total_tracks'] = 5
    metadata['lead_performer_region'] = ("CA", "QC")
    metadata['production_company'] = "Effendi Records Inc."
    metadata['music_producer'] = "Joel Miller & Paul Johnston"

    _assert_can_be_saved_and_reloaded_with_same_state(flac, metadata)


def test_removes_comment_field_when_tag_not_in_metadata(flac):
    filename = flac(ARTIST="Joel Miller")
    container.save(filename, Metadata())
    _assert_contains_metadata(filename, Metadata())


def test_stores_several_pictures(flac):
    filename = flac()
    metadata = Metadata()
    metadata.addImage('image/jpeg', b'front-1.jpg', desc='Front Cover')
    metadata.addImage('image/jpeg', b'front-2.jpg', desc='Front Cover')

    container.save(filename, metadata)

    assert_that(container.load(filename).images, contains_inanyorder(
        Image('image/jpeg', b'front-1.jpg', type_=Image.OTHER, desc='Front Cover'),
        Image('image/jpeg', b'front-2.jpg', type_=Image.OTHER, desc='Front Cover (2)'),
    ))


def test_overwrites_existing_attached_pictures(flac):
    filename = flac(PICTURES=(
        ('image/jpeg', PictureType.FRONT_COVER, 'Front', b'front.jpg'),
        ('image/jpeg', PictureType.BACK_COVER, 'Back', b'back.jpg')))

    metadata = Metadata()

    container.save(filename, metadata)
    assert_that(container.load(filename).images, has_length(0), 'removed images')

    metadata.addImage(mime='image/jpeg', data=b'front.jpg', desc='Front')
    container.save(filename, metadata)

    assert_that(container.load(filename).images, has_length(1), 'updated images')


def _assert_can_be_saved_and_reloaded_with_same_state(flac, metadata):
    filename = flac()
    container.save(filename, metadata.copy())
    _assert_contains_metadata(filename, metadata)


def _assert_contains_metadata(filename, metadata):
    expected_metadata = metadata.copy()
    expected_metadata['bitrate'] = BITRATE
    expected_metadata['duration'] = DURATION

    actual_metadata = container.load(filename)
    assert_that(actual_metadata, has_entries(**expected_metadata), 'metadata in file')
