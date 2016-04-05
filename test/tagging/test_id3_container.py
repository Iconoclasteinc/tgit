import pytest
from hamcrest import (assert_that, has_entry, has_key, has_length, contains, is_not, contains_inanyorder, has_entries,
                      not_, all_of)
from mutagen.mp3 import MP3

from testing import mp3_file
from tgit.metadata import Metadata, Image
from tgit.tagging.id3_container import ID3Container

pytestmark = pytest.mark.unit


BITRATE = mp3_file.Base.bitrate
DURATION = mp3_file.Base.duration

container = ID3Container()


@pytest.yield_fixture
def mp3(tmpdir):
    def maker(**tags):
        return mp3_file.make(to=tmpdir.strpath, **tags).filename

    yield maker
    tmpdir.remove()


def test_reads_album_title_from_talb_frame(mp3):
    metadata = container.load(mp3(TALB="Album"))
    assert_that(metadata, has_entry("release_name", "Album"), "metadata")


def test_joins_all_texts_of_frames(mp3):
    metadata = container.load(mp3(TALB=["Album", "Titles"]))
    assert_that(metadata, has_entry("release_name", "Album\x00Titles"), "metadata")


def test_reads_lead_performer_from_tpe1_frame(mp3):
    metadata = container.load(mp3(TPE1="Lead Artist"))
    assert_that(metadata, has_entry("lead_performer", "Lead Artist"), "metadata")


def test_reads_guest_performers_from_tmcl_frame(mp3):
    metadata = container.load(mp3(TMCL=[["Guitar", "Guitarist"], ["Guitar", "Bassist"],
                                        ["Piano", "Pianist"]]))
    assert_that(metadata, has_entry("guest_performers", contains_inanyorder(
        ("Guitar", "Guitarist"),
        ("Guitar", "Bassist"),
        ("Piano", "Pianist"))), "metadata")


def test_ignores_tmcl_entries_with_blank_names(mp3):
    metadata = container.load(mp3(TMCL=[["Guitar", "Guitarist"], ["Piano", ""]]))
    assert_that(metadata, has_entry("guest_performers", contains(("Guitar", "Guitarist"))), "metadata")


def test_reads_label_name_from_town_frame(mp3):
    metadata = container.load(mp3(TOWN="Label Name"))
    assert_that(metadata, has_entry("label_name", "Label Name"), "metadata")


def test_reads_catalog_number_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_CATALOG_NUMBER="123 456-1"))
    assert_that(metadata, has_entry("catalog_number", "123 456-1"), "metadata")


def test_reads_upc_from_custom_barcode_frame(mp3):
    metadata = container.load(mp3(TXXX_BARCODE="1234567899999"))
    assert_that(metadata, has_entry("upc", "1234567899999"), "metadata")


def test_reads_recording_time_from_tdrc_frame(mp3):
    metadata = container.load(mp3(TDRC="2012-07-15"))
    assert_that(metadata, has_entry("recording_time", "2012-07-15"), "metadata")


def test_reads_release_time_from_tdrl_frame(mp3):
    metadata = container.load(mp3(TDRL="2013-11-15"))
    assert_that(metadata, has_entry("release_time", "2013-11-15"), "metadata")


def test_reads_original_release_time_from_tdor_frame(mp3):
    metadata = container.load(mp3(TDOR="1999-03-15"))
    assert_that(metadata, has_entry("original_release_time", "1999-03-15"), "metadata")


def test_reads_recording_studio_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_RECORDING_STUDIO="Studio Name"))
    assert_that(metadata, has_entry("recording_studio", "Studio Name"), "metadata")


def test_reads_music_producer_from_tipl_frame(mp3):
    metadata = container.load(mp3(TIPL=[["producer", "Music Producer"]]))
    assert_that(metadata, has_entry("music_producer", "Music Producer"), "metadata")


def test_takes_into_account_last_of_multiple_role_definitions(mp3):
    metadata = container.load(mp3(TIPL=[["producer", "first"], ["producer", "last"]]))
    assert_that(metadata, has_entry("music_producer", "last"), "metadata")


def test_ignores_tpil_entries_with_blank_names(mp3):
    metadata = container.load(mp3(TIPL=[["producer", ""]]))
    assert_that(metadata, is_not(has_key("producer")), "metadata")


def test_reads_mixing_engineer_from_tipl_frame(mp3):
    metadata = container.load(mp3(TIPL=[["mix", "Mixing Engineer"]]))
    assert_that(metadata, has_entry("mixer", "Mixing Engineer"), "metadata")


def test_reads_comments_from_french_comm_frame(mp3):
    metadata = container.load(mp3(COMM=("Comments", "fra")))
    assert_that(metadata, has_entry("comments", "Comments"), "metadata")


def test_reads_track_title_from_tit2_frame(mp3):
    metadata = container.load(mp3(TIT2="Track Title"))
    assert_that(metadata, has_entry("track_title", "Track Title"), "metadata")


def test_reads_version_info_from_tpe4_frame(mp3):
    metadata = container.load(mp3(TPE4="Version Info"))
    assert_that(metadata, has_entry("version_info", "Version Info"), "metadata")


def test_reads_featured_guest_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_FEATURED_GUEST="Featured Guest"))
    assert_that(metadata, has_entry("featured_guest", "Featured Guest"), "metadata")


def test_reads_lyricist_from_text_frame(mp3):
    metadata = container.load(mp3(TEXT="Lyricist"))
    assert_that(metadata, has_entry("lyricist", "Lyricist"), "metadata")


def test_reads_composer_from_tcom_frame(mp3):
    metadata = container.load(mp3(TCOM="Composer"))
    assert_that(metadata, has_entry("composer", "Composer"), "metadata")


def test_reads_publisher_from_tpub_frame(mp3):
    metadata = container.load(mp3(TPUB="Publisher"))
    assert_that(metadata, has_entry("publisher", "Publisher"), "metadata")


def test_reads_isrc_from_tsrc_frame(mp3):
    metadata = container.load(mp3(TSRC="AABB12345678"))
    assert_that(metadata, has_entry("isrc", "AABB12345678"), "metadata")


def test_reads_tags_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_TAGS="Tag1 Tag2 Tag3"))
    assert_that(metadata, has_entry("labels", "Tag1 Tag2 Tag3"), "metadata")


def test_reads_isni_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_ISNI_Joel_Miller="00000123456789"))
    assert_that(metadata, has_entry("isnis", has_entry("Joel Miller", "00000123456789")), "metadata")


def test_reads_iswc_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_ISWC="T-345246800-1"))
    assert_that(metadata, has_entry("iswc", "T-345246800-1"), "metadata")


def test_reads_lyrics_from_uslt_french_frame(mp3):
    metadata = container.load(mp3(USLT=("Lyrics", "fra")))
    assert_that(metadata, has_entry("lyrics", "Lyrics"), "metadata")


def test_reads_language_from_tlan_frame(mp3):
    metadata = container.load(mp3(TLAN="fra"))
    assert_that(metadata, has_entry("language", "fra"), "metadata")


def test_reads_primary_style_from_tcon_frame(mp3):
    metadata = container.load(mp3(TCON="Jazz"))
    assert_that(metadata, has_entry("primary_style", "Jazz"), "metadata")


def test_reads_compilation_flag_from_non_standard_tcmp_frame(mp3):
    metadata = container.load(mp3(TCMP="0"))
    assert_that(metadata, has_entry("compilation", False), "metadata")
    metadata = container.load(mp3(TCMP="1"))
    assert_that(metadata, has_entry("compilation", True), "metadata")


def test_reads_bitrate_from_audio_stream_information(mp3):
    metadata = container.load(mp3())
    assert_that(metadata, has_entry("bitrate", BITRATE), "bitrate")


def test_reads_duration_from_audio_stream_information(mp3):
    metadata = container.load(mp3())
    assert_that(metadata, has_entry("duration", DURATION), "duration")


def test_reads_cover_pictures_from_apic_frames(mp3):
    metadata = container.load(mp3(
        APIC_FRONT=("image/jpeg", "Front", b"front-cover.jpg"),
        APIC_BACK=("image/jpeg", "Back", b"back-cover.jpg")))

    assert_that(metadata.images, contains_inanyorder(
        Image("image/jpeg", b"front-cover.jpg", type_=Image.FRONT_COVER, desc="Front"),
        Image("image/jpeg", b"back-cover.jpg", type_=Image.BACK_COVER, desc="Back"),
    ))


def test_reads_tagger_name_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_TAGGER="TGiT"))
    assert_that(metadata, has_entry("tagger", "TGiT"), "metadata")


def test_reads_tagger_version_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_TAGGER_VERSION="1.0"))
    assert_that(metadata, has_entry("tagger_version", "1.0"), "metadata")


def test_reads_tagging_time_from_tdtg_frame(mp3):
    metadata = container.load(mp3(TDTG="2014-03-26T18:18:55"))
    assert_that(metadata, has_entry("tagging_time", "2014-03-26 18:18:55"), "metadata")


def test_reads_track_number_from_trck_frame(mp3):
    metadata = container.load(mp3(TRCK="3"))
    assert_that(metadata, has_entry("track_number", 3), "metadata")


def test_reads_total_tracks_from_trck_frame(mp3):
    metadata = container.load(mp3(TRCK="3/5"))
    assert_that(metadata, has_entry("total_tracks", 5), "metadata")


def test_reads_lead_performer_region_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_LEAD_PERFORMER_REGION="CA-QC"))
    assert_that(metadata, has_entry("lead_performer_region", ("CA", "QC")), "metadata")


def test_reads_production_company_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_PRODUCTION_COMPANY="Effendi Records Inc."))
    assert_that(metadata, has_entry("production_company", "Effendi Records Inc."), "metadata")


def test_reads_production_company_region_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_PRODUCTION_COMPANY_REGION="CA-QC"))
    assert_that(metadata, has_entry("production_company_region", ("CA", "QC")), "metadata")


def test_reads_recording_studio_region_from_custom_frame(mp3):
    metadata = container.load(mp3(TXXX_RECORDING_STUDIO_REGION="CA-QC"))
    assert_that(metadata, has_entry("recording_studio_region", ("CA", "QC")), "metadata")


def test_round_trips_empty_metadata_to_file(mp3):
    assert_can_be_saved_and_reloaded_with_same_state(mp3, Metadata())


def test_round_trips_metadata_to_file(mp3):
    metadata = Metadata()
    metadata.addImage("image/jpeg", b"salers.jpg", Image.FRONT_COVER)
    metadata["release_name"] = "Album"
    metadata["compilation"] = True
    metadata["lead_performer"] = "Lead Performer"
    metadata["lead_performer_region"] = ("CA", "QC")
    metadata["isnis"] = {"Lead Performer": "0000123456789",
                         "Lyricist": "0000123456789"}
    metadata["ipis"] = {"Lyricist": "0000123456789"}
    metadata["iswc"] = "T-345246800-1"
    metadata["guest_performers"] = [("Guitar", "Guitarist"), ("Guitar", "Bassist"), ("Piano", "Pianist")]
    metadata["label_name"] = "Label Name"
    metadata["production_company"] = "Production Company"
    metadata["production_company_region"] = ("CA", "QC")
    metadata["catalog_number"] = "123 456-1"
    metadata["upc"] = "987654321111"
    metadata["recording_time"] = "2012-07-01"
    metadata["release_time"] = "2013-12-01"
    metadata["original_release_time"] = "1999-01-01"
    metadata["recording_studio"] = "Studio Name"
    metadata["recording_studio_region"] = ("CA", "QC")
    metadata["music_producer"] = "Music Producer"
    metadata["mixer"] = "Mixing Engineer"
    metadata["contributors"] = [("recording", "Recording Eng."),
                                ("mastering", "Mastering Eng."),
                                ("recording", "Assistant Recording Eng.")]
    metadata["comments"] = "Comments"
    metadata["primary_style"] = "Jazz"
    metadata["track_title"] = "Track Title"
    metadata["version_info"] = "Version Info"
    metadata["featured_guest"] = "Featured Guest"
    metadata["lyricist"] = "Lyricist"
    metadata["composer"] = "Composer"
    metadata["publisher"] = "Publisher"
    metadata["isrc"] = "ZZXX87654321"
    metadata["labels"] = "Tag1 Tag2 Tag3"
    metadata["lyrics"] = "Lyrics"
    metadata["language"] = "fra"
    metadata["tagger"] = "TGiT"
    metadata["tagger_version"] = "1.0"
    metadata["tagging_time"] = "2014-03-26 18:18:55"
    metadata["track_number"] = 3
    metadata["total_tracks"] = 5

    assert_can_be_saved_and_reloaded_with_same_state(mp3, metadata)


def test_handles_unicode_metadata(mp3):
    metadata = Metadata()
    metadata["release_name"] = "Titre en Français"
    assert_can_be_saved_and_reloaded_with_same_state(mp3, metadata)


def test_removes_frame_when_tag_not_in_metadata(mp3):
    filename = mp3(TALB="Album",
                   TMCL=[["Guitar", "Guitarist"]],
                   TIPL=[["mix", "Mixing Engineer"]],
                   USLT=("", "fra"))

    container.save(filename, Metadata())
    assert_contains_metadata(filename, Metadata())


def test_takes_none_as_absence_of_tag(mp3):
    filename = mp3()
    container.save(filename, Metadata(compilation=None))
    assert_contains_metadata(filename, Metadata())


def test_stores_several_pictures_sharing_the_same_description(mp3):
    filename = mp3()
    metadata = Metadata()
    metadata.addImage("image/jpeg", b"salers.jpg", desc="Front Cover")
    metadata.addImage("image/jpeg", b"ragber.jpg", desc="Front Cover")

    container.save(filename, metadata)

    assert_that(container.load(filename).images, contains_inanyorder(
        Image("image/jpeg", b"salers.jpg", type_=Image.OTHER, desc="Front Cover"),
        Image("image/jpeg", b"ragber.jpg", type_=Image.OTHER, desc="Front Cover (2)"),
    ))


def test_overwrites_existing_attached_pictures(mp3):
    filename = mp3(APIC_FRONT=("image/jpeg", "", b"front-cover.jpg"))
    metadata = Metadata()

    container.save(filename, metadata)
    assert_that(container.load(filename).images, has_length(0), "removed images")

    metadata.addImage(mime="image/jpeg", data=b"salers.jpg", desc="Front")
    container.save(filename, metadata)

    assert_that(container.load(filename).images, has_length(1), "updated images")


def test_transforms_deprecated_tagger_frame_into_tagger_and_version(mp3):
    metadata = container.load(mp3(TXXX_Tagger="TGiT v1.1"))
    assert_that(metadata, has_entries(tagger="TGiT", tagger_version="1.1"), "metadata")


def test_upgrades_deprecated_frames_to_their_new_form(mp3):
    metadata = container.load(mp3(TXXX_UPC="987654321111",
                                  TXXX_TAGGING_TIME="2014-03-26 14:18:55 -0400"))

    assert_that(metadata, has_entries(upc="987654321111", tagging_time="2014-03-26 18:18:55"), "metadata")


def test_upgrades_deprecated_isni_frames_to_its_new_form(mp3):
    metadata = container.load(mp3(TPE1="Joel Miller",
                                  TXXX_ISNI="0000000123456789"))

    assert_that(metadata, has_entries(lead_performer="Joel Miller",
                                      isnis=has_entry("Joel Miller", "0000000123456789")), "metadata")


def test_removes_old_isni_frames(mp3):
    filename = mp3(TXXX_ISNI_Joel_Miller="00000123456789",
                   TXXX_ISNI_Rebecca_Ann_Maloy="98765432100000")
    container.save(filename, Metadata(isnis={"Joel Miller": "00000123456789"}))

    tags = MP3(filename)
    assert_that(tags, all_of(has_key("TXXX:ISNI:Joel Miller"),
                             not_(has_key("TXXX:ISNI:Rebecca Ann Maloy"))), "tags in file")


def test_removes_old_ipi_frames(mp3):
    filename = mp3(TXXX_IPI_Joel_Miller="00000123456789",
                   TXXX_IPI_Rebecca_Ann_Maloy="98765432100000")
    container.save(filename, Metadata(ipis={"Joel Miller": "00000123456789"}))

    tags = MP3(filename)
    assert_that(tags, all_of(has_key("TXXX:IPI:Joel Miller"),
                             not_(has_key("TXXX:IPI:Rebecca Ann Maloy"))), "tags in file")


def test_removes_deprecated_frames_on_save(mp3):
    filename = mp3(TXXX_Tagger="TGiT v1.1",
                   TXXX_TAGGING_TIME="2014-03-26 14:18:55 EDT-0400",
                   TXXX_UPC="987654321111")
    container.save(filename, Metadata())

    tags = MP3(filename)
    assert_that(tags, all_of(not_(has_key("TXXX:Tagger")),
                             not_(has_key("TXXX:TAGGING_TIME")),
                             not_(has_key("TXXX:UPC"))), "tags in file")


def assert_can_be_saved_and_reloaded_with_same_state(mp3, metadata):
    filename = mp3()
    container.save(filename, metadata.copy())
    assert_contains_metadata(filename, metadata)


def assert_contains_metadata(filename, metadata):
    expected_metadata = metadata.copy()
    expected_metadata["bitrate"] = BITRATE
    expected_metadata["duration"] = DURATION

    actual_metadata = container.load(filename)
    assert_that(actual_metadata, has_entries(**expected_metadata), "metadata in file")
