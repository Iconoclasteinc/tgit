# -*- coding: utf-8 -*-

import shutil

from hamcrest import assert_that, has_entry, has_key, has_length, contains, is_not, contains_inanyorder, \
    equal_to
import pytest

from test.util import mp3_file

from tgit.tagging.id3_container import ID3Container
from tgit.metadata import Metadata, Image

BITRATE = mp3_file.base.bitrate
DURATION = mp3_file.base.duration

container = ID3Container()


@pytest.yield_fixture
def mp3(tmpdir):
    def maker(**tags):
        return mp3_file.make(to=tmpdir.strpath, **tags).filename

    yield maker
    shutil.rmtree(tmpdir.strpath)


def test_reads_album_title_from_t_a_l_b_frame(mp3):
    metadata = container.load(mp3(TALB='Album'))
    assert_that(metadata, has_entry('release_name', 'Album'), 'metadata')


def test_joins_all_texts_of_frames(mp3):
    metadata = container.load(mp3(TALB=['Album', 'Titles']))
    assert_that(metadata, has_entry('release_name', 'Album\x00Titles'), 'metadata')


def test_reads_lead_performer_from_tpe1_frame(mp3):
    metadata = container.load(mp3(TPE1='Lead Artist'))
    assert_that(metadata, has_entry('lead_performer', 'Lead Artist'), 'metadata')


def test_reads_guest_performers_from_t_m_c_l_frame(mp3):
    metadata = container.load(mp3(TMCL=[['Guitar', 'Guitarist'], ['Guitar', 'Bassist'],
                                        ['Piano', 'Pianist']]))
    assert_that(metadata, has_entry('guestPerformers', contains_inanyorder(
        ('Guitar', 'Guitarist'),
        ('Guitar', 'Bassist'),
        ('Piano', 'Pianist'))), 'metadata')


def test_ignores_t_m_c_l_entries_with_blank_names(mp3):
    metadata = container.load(mp3(TMCL=[['Guitar', 'Guitarist'], ['Piano', '']]))
    assert_that(metadata, has_entry('guestPerformers', contains(('Guitar', 'Guitarist'))), 'metadata')


def test_reads_label_name_from_t_o_w_n_frame(mp3):
    metadata = container.load(mp3(TOWN='Label Name'))
    assert_that(metadata, has_entry('label_name', 'Label Name'), 'metadata')


def test_reads_catalog_number_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_CATALOG_NUMBER='123 456-1'))
    assert_that(metadata, has_entry('catalogNumber', '123 456-1'), 'metadata')


def test_reads_upc_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_UPC='1234567899999'))
    assert_that(metadata, has_entry('upc', '1234567899999'), 'metadata')


def test_reads_recording_time_from_t_d_r_c_frame(mp3):
    metadata = container.load(mp3(TDRC='2012-07-15'))
    assert_that(metadata, has_entry('recording_time', '2012-07-15'), 'metadata')


def test_reads_release_time_from_t_d_r_l_frame(mp3):
    metadata = container.load(mp3(TDRL='2013-11-15'))
    assert_that(metadata, has_entry('releaseTime', '2013-11-15'), 'metadata')


def test_reads_original_release_time_from_t_d_o_r_frame(mp3):
    metadata = container.load(mp3(TDOR='1999-03-15'))
    assert_that(metadata, has_entry('originalReleaseTime', '1999-03-15'), 'metadata')


def test_reads_recording_studios_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_RECORDING_STUDIOS='Studio Name'))
    assert_that(metadata, has_entry('recordingStudios', 'Studio Name'), 'metadata')


def test_reads_artistic_producer_from_t_i_p_l_frame(mp3):
    metadata = container.load(mp3(TIPL=[['producer', 'Artistic Producer']]))
    assert_that(metadata, has_entry('producer', 'Artistic Producer'), 'metadata')


def test_takes_into_account_last_of_multiple_role_definitions(mp3):
    metadata = container.load(mp3(TIPL=[['producer', 'first'], ['producer', 'last']]))
    assert_that(metadata, has_entry('producer', 'last'), 'metadata')


def test_ignores_tpil_entries_with_blank_names(mp3):
    metadata = container.load(mp3(TIPL=[['producer', '']]))
    assert_that(metadata, is_not(has_key('producer')), 'metadata')


def test_reads_mixing_engineer_from_t_i_p_l_frame(mp3):
    metadata = container.load(mp3(TIPL=[['mix', 'Mixing Engineer']]))
    assert_that(metadata, has_entry('mixer', 'Mixing Engineer'), 'metadata')


def test_reads_comments_from_french_c_o_m_m_frame(mp3):
    metadata = container.load(mp3(COMM=('Comments', 'fra')))
    assert_that(metadata, has_entry('comments', 'Comments'), 'metadata')


def test_reads_track_title_from_t_i_t_2_frame(mp3):
    metadata = container.load(mp3(TIT2='Track Title'))
    assert_that(metadata, has_entry('track_title', 'Track Title'), 'metadata')


def test_reads_version_info_from_t_p_e_4_frame(mp3):
    metadata = container.load(mp3(TPE4='Version Info'))
    assert_that(metadata, has_entry('versionInfo', 'Version Info'), 'metadata')


def test_reads_featured_guest_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_FEATURED_GUEST='Featured Guest'))
    assert_that(metadata, has_entry('featuredGuest', 'Featured Guest'), 'metadata')


def test_reads_lyricist_from_t_e_x_t_frame(mp3):
    metadata = container.load(mp3(TEXT='Lyricist'))
    assert_that(metadata, has_entry('lyricist', 'Lyricist'), 'metadata')


def test_reads_composer_from_t_c_o_m_frame(mp3):
    metadata = container.load(mp3(TCOM='Composer'))
    assert_that(metadata, has_entry('composer', 'Composer'), 'metadata')


def test_reads_publisher_from_t_p_u_b_frame(mp3):
    metadata = container.load(mp3(TPUB='Publisher'))
    assert_that(metadata, has_entry('publisher', 'Publisher'), 'metadata')


def test_reads_isrc_from_t_s_r_c_frame(mp3):
    metadata = container.load(mp3(TSRC='AABB12345678'))
    assert_that(metadata, has_entry('isrc', 'AABB12345678'), 'metadata')


def test_reads_tags_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_TAGS='Tag1 Tag2 Tag3'))
    assert_that(metadata, has_entry('labels', 'Tag1 Tag2 Tag3'), 'metadata')


def test_reads_isni_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_ISNI='00000123456789'))
    assert_that(metadata, has_entry('isni', '00000123456789'), 'metadata')


def test_reads_lyrics_from_u_s_l_t_french_frame(mp3):
    metadata = container.load(mp3(USLT=('Lyrics', 'fra')))
    assert_that(metadata, has_entry('lyrics', 'Lyrics'), 'metadata')


def test_reads_language_from_t_l_a_n_frame(mp3):
    metadata = container.load(mp3(TLAN='fra'))
    assert_that(metadata, has_entry('language', 'fra'), 'metadata')


def test_reads_primary_style_from_t_c_o_n_frame(mp3):
    metadata = container.load(mp3(TCON='Jazz'))
    assert_that(metadata, has_entry('primary_style', 'Jazz'), 'metadata')


def test_reads_compilation_flag_from_non_standard_t_c_m_p_frame(mp3):
    metadata = container.load(mp3(TCMP='0'))
    assert_that(metadata, has_entry('compilation', False), 'metadata')
    metadata = container.load(mp3(TCMP='1'))
    assert_that(metadata, has_entry('compilation', True), 'metadata')


def test_reads_bitrate_from_audio_stream_information(mp3):
    metadata = container.load(mp3())
    assert_that(metadata, has_entry('bitrate', BITRATE), 'bitrate')


def test_reads_duration_from_audio_stream_information(mp3):
    metadata = container.load(mp3())
    assert_that(metadata, has_entry('duration', DURATION), 'duration')


def test_reads_cover_pictures_from_a_p_i_c_frames(mp3):
    metadata = container.load(mp3(
        APIC_FRONT=('image/jpeg', 'Front', b'front-cover.jpg'),
        APIC_BACK=('image/jpeg', 'Back', b'back-cover.jpg')))

    assert_that(metadata.images, contains_inanyorder(
        Image('image/jpeg', b'front-cover.jpg', type_=Image.FRONT_COVER, desc='Front'),
        Image('image/jpeg', b'back-cover.jpg', type_=Image.BACK_COVER, desc='Back'),
    ))


def test_reads_tagger_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_TAGGER='TGiT v1.0'))
    assert_that(metadata, has_entry('tagger', 'TGiT v1.0'), 'metadata')


def test_reads_tagging_time_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_TAGGING_TIME='2014-03-26 14:18:55 EDT-0400'))
    assert_that(metadata, has_entry('taggingTime', '2014-03-26 14:18:55 EDT-0400'), 'metadata')


def test_round_trips_empty_metadata_to_file(mp3):
    assert_can_be_saved_and_reloaded_with_same_state(mp3, Metadata())


def test_round_trips_metadata_to_file(mp3):
    metadata = Metadata()
    metadata.addImage('image/jpeg', b'salers.jpg', Image.FRONT_COVER)
    metadata['release_name'] = 'Album'
    metadata['compilation'] = True
    metadata['lead_performer'] = 'Lead Performer'
    metadata['isni'] = '0000123456789'
    metadata['guestPerformers'] = [('Guitar', 'Guitarist'), ('Guitar', 'Bassist'), ('Piano', 'Pianist')]
    metadata['label_name'] = 'Label Name'
    metadata['catalogNumber'] = '123 456-1'
    metadata['upc'] = '987654321111'
    metadata['recording_time'] = '2012-07-01'
    metadata['releaseTime'] = '2013-12-01'
    metadata['originalReleaseTime'] = '1999-01-01'
    metadata['recordingStudios'] = 'Studio Name'
    metadata['producer'] = 'Artistic Producer'
    metadata['mixer'] = 'Mixing Engineer'
    metadata['contributors'] = [('recording', 'Recording Eng.'),
                                ('mastering', 'Mastering Eng.'),
                                ('recording', 'Assistant Recording Eng.')]
    metadata['comments'] = 'Comments'
    metadata['primary_style'] = 'Jazz'
    metadata['track_title'] = 'Track Title'
    metadata['versionInfo'] = 'Version Info'
    metadata['featuredGuest'] = 'Featured Guest'
    metadata['lyricist'] = 'Lyricist'
    metadata['composer'] = 'Composer'
    metadata['publisher'] = 'Publisher'
    metadata['isrc'] = 'ZZXX87654321'
    metadata['labels'] = 'Tag1 Tag2 Tag3'
    metadata['lyrics'] = 'Lyrics'
    metadata['language'] = 'fra'
    metadata['tagger'] = 'TGiT v1.0'
    metadata['taggingTime'] = '2014-03-26 14:18:55 EDT-0400'

    assert_can_be_saved_and_reloaded_with_same_state(mp3, metadata)


def test_handles_unicode_metadata(mp3):
    metadata = Metadata()
    metadata['release_name'] = 'Titre en Français'
    assert_can_be_saved_and_reloaded_with_same_state(mp3, metadata)


def test_removes_frame_when_tag_not_in_metadata(mp3):
    filename = mp3(TALB='Album',
                   TMCL=[['Guitar', 'Guitarist']],
                   TIPL=[['mix', 'Mixing Engineer']],
                   USLT=('', 'fra'))

    container.save(filename, Metadata())
    assert_contains_metadata(filename, Metadata())


def test_takes_none_as_absence_of_tag(mp3):
    filename = mp3()
    container.save(filename, Metadata(compilation=None))
    assert_contains_metadata(filename, Metadata())


def test_stores_several_pictures_sharing_the_same_description(mp3):
    filename = mp3()
    metadata = Metadata()
    metadata.addImage('image/jpeg', b'salers.jpg', desc='Front Cover')
    metadata.addImage('image/jpeg', b'ragber.jpg', desc='Front Cover')

    container.save(filename, metadata)

    assert_that(container.load(filename).images, contains_inanyorder(
        Image('image/jpeg', b'salers.jpg', type_=Image.OTHER, desc='Front Cover'),
        Image('image/jpeg', b'ragber.jpg', type_=Image.OTHER, desc='Front Cover (2)'),
    ))


def test_overwrites_existing_attached_pictures(mp3):
    filename = mp3(APIC_FRONT=('image/jpeg', '', b'front-cover.jpg'))
    metadata = Metadata()

    container.save(filename, metadata)
    assert_that(container.load(filename).images, has_length(0), 'removed images')

    metadata.addImage(mime='image/jpeg', data=b'salers.jpg', desc='Front')
    container.save(filename, metadata)

    assert_that(container.load(filename).images, has_length(1), 'updated images')


def assert_can_be_saved_and_reloaded_with_same_state(mp3, metadata):
    filename = mp3()
    container.save(filename, metadata.copy())
    assert_contains_metadata(filename, metadata)


def assert_contains_metadata(filename, metadata):
    expected_metadata = metadata.copy()
    expected_metadata['bitrate'] = BITRATE
    expected_metadata['duration'] = DURATION

    actual_metadata = container.load(filename)
    assert_that(actual_metadata, equal_to(expected_metadata), 'actual metadata')