# -*- coding: utf-8 -*-
from hamcrest import starts_with, any_of

from cute import gestures
from cute.matchers import named, with_buddy, showing_on_screen
from cute.platforms import linux
from testing.drivers.contributors_tab_driver import contributor_tab
from tgit.ui.pages.track_edition_page import TrackEditionPage
from ._screen_driver import ScreenDriver


def track_edition_page(parent, number=None):
    name_condition = starts_with("track_edition_page") if not number else "track_edition_page_" + str(number)
    return TrackEditionPageDriver.find_single(parent, TrackEditionPage, named(name_condition), showing_on_screen())


def track_edition_page_numbered(parent, number):
    return TrackEditionPageDriver.find_single(parent, TrackEditionPage, named("track_edition_page_" + str(number)),
                                              showing_on_screen())


def no_track_edition_page(parent):
    return TrackEditionPageDriver.find_none(parent, TrackEditionPage, named(starts_with("track_edition_page")))


class TrackEditionPageDriver(ScreenDriver):
    TAB_SELECTION_DELAY = 15 if linux else 0

    def shows_metadata(self, **meta):
        for tag, value in meta.items():
            if tag == "track_title":
                self.shows_track_title(value)
            elif tag == "lead_performer":
                self.shows_lead_performer(value)
            elif tag == "version_info":
                self.shows_version_info(value)
            elif tag == "featured_guest":
                self.shows_featured_guest(value)
            elif tag == "lyricist":
                self.shows_lyricist(value)
            elif tag == "composer":
                self.shows_composer(value)
            elif tag == "publichser":
                self.shows_publisher(value)
            elif tag == "isrc":
                self.shows_isrc(value)
            elif tag == "bitrate":
                self.shows_bitrate(value)
            elif tag == "duration":
                self.shows_duration(value)
            elif tag == "track_number":
                self.shows_track_number(value)
            elif tag == "recording_studio":
                self.shows_recording_studio(value)
            elif tag == "music_producer":
                self.shows_music_producer(value)
            elif tag == "mixer":
                self.shows_mixer(value)
            elif tag == "primary_style":
                self.shows_primary_style(value)
            else:
                raise AssertionError("Don't know how to verify {0}".format(tag))

    def change_metadata(self, **meta):
        for tag, value in meta.items():
            if tag == "track_title":
                self.change_track_title(value)
            elif tag == "lead_performer":
                self.change_lead_performer(value)
            elif tag == "version_info":
                self.change_version_info(value)
            elif tag == "featured_guest":
                self.change_featured_guest(value)
            elif tag == "lyricist":
                self.change_lyricist(value)
            elif tag == "lyricist_ipi":
                pass
            elif tag == "composer":
                self.change_composer(value)
            elif tag == "publisher":
                self.change_publisher(value)
            elif tag == "isrc":
                self.change_isrc(value)
            elif tag == "recording_studio":
                self.change_recording_studio(value)
            elif tag == "music_producer":
                self.change_music_producer(value)
            elif tag == "mixer":
                self.change_mixer(value)
            elif tag == "primary_style":
                self.select_primary_style(value)
            else:
                raise AssertionError("Don't know how to edit <{0}>".format(tag))

        # must be done after lyricist to let the application enable the field
        if "lyricist_ipi" in meta:
            self.change_lyricist_ipi(meta["lyricist_ipi"])

    def shows_album_lead_performer(self, name):
        label = self.label(named("_album_main_artist"))
        label.is_showing_on_screen()
        label.has_text(name)

    def shows_album_title(self, title):
        label = self.label(named("_album_title"))
        label.is_showing_on_screen()
        label.has_text(title)

    def shows_track_number(self, number):
        label = self.label(named("_track_number"))
        label.is_showing_on_screen()
        label.has_text(any_of(starts_with("Track " + str(number)), starts_with("Piste " + str(number))))

    def shows_track_title(self, track_title):
        self.label(with_buddy(named("_track_title"))).is_showing_on_screen()
        self.lineEdit(named("_track_title")).has_text(track_title)

    def change_track_title(self, title):
        self.lineEdit(named("_track_title")).change_text(title)

    def shows_lead_performer(self, name, disabled=False):
        label = self.label(with_buddy(named("_main_artist")))
        label.is_showing_on_screen()
        label.is_disabled(disabled)
        info = self.label(named("_main_artist_info"))
        info.is_showing_on_screen()
        info.is_disabled(disabled)
        help_label = self.label(named("_main_artist_help"))
        help_label.is_showing_on_screen()
        help_label.is_disabled(disabled)
        edit = self.lineEdit(named("_main_artist"))
        edit.has_text(name)
        edit.is_disabled(disabled)

    def change_lead_performer(self, name):
        self.lineEdit(named("_main_artist")).change_text(name)

    def shows_version_info(self, info):
        self.label(with_buddy(named("_version"))).is_showing_on_screen()
        self.lineEdit(named("_version")).has_text(info)

    def change_version_info(self, info):
        self.lineEdit(named("_version")).change_text(info)

    def shows_featured_guest(self, name):
        self.label(with_buddy(named("_featured_guest"))).is_showing_on_screen()
        self.lineEdit(named("_featured_guest")).has_text(name)

    def change_featured_guest(self, name):
        self.lineEdit(named("_featured_guest")).change_text(name)

    def shows_comments(self, comments):
        self.label(with_buddy(named("_comments"))).is_showing_on_screen()
        self.textEdit(named("_comments")).has_plain_text(comments)

    def change_comments(self, *comments):
        edit = self.textEdit(named("_comments"))
        edit.clear_all_text()
        for comment in comments:
            edit.add_line(comment)
        edit.perform(gestures.tab())

    def shows_lyricist(self, name):
        self._select_contributors_tab()
        self.label(with_buddy(named("_lyricist"))).is_showing_on_screen()
        self.lineEdit(named("_lyricist")).has_text(name)

    def change_lyricist(self, name):
        self._select_contributors_tab()
        contributor_tab(self).add_lyricist(name)

    def change_lyricist_ipi(self, ipi):
        self._select_contributors_tab()
        contributor_tab(self).change_ipi_at_row(ipi, 0)

    def shows_composer(self, name):
        self._select_contributors_tab()
        self.label(with_buddy(named("_composer"))).is_showing_on_screen()
        self.lineEdit(named("_composer")).has_text(name)

    def change_composer(self, name):
        self._select_contributors_tab()
        self.lineEdit(named("_composer")).change_text(name)

    def change_composer_ipi(self, ipi):
        self._select_contributors_tab()
        self.lineEdit(named("_composer_ipi")).change_text(ipi)

    def shows_composer_ipi(self, ipi):
        self._select_contributors_tab()
        self.lineEdit(named("_composer_ipi")).has_text(ipi)

    def shows_composer_isni(self, isni):
        self._select_contributors_tab()
        self.lineEdit(named("_composer_isni")).has_text(isni)

    def shows_publisher(self, name):
        self._select_contributors_tab()
        self.label(with_buddy(named("_publisher"))).is_showing_on_screen()
        self.lineEdit(named("_publisher")).has_text(name)

    def change_publisher(self, name):
        self._select_contributors_tab()
        self.lineEdit(named("_publisher")).change_text(name)

    def change_publisher_ipi(self, ipi):
        self._select_contributors_tab()
        self.lineEdit(named("_publisher_ipi")).change_text(ipi)

    def shows_publisher_ipi(self, ipi):
        self._select_contributors_tab()
        self.lineEdit(named("_publisher_ipi")).has_text(ipi)

    def shows_publisher_isni(self, isni):
        self._select_contributors_tab()
        self.lineEdit(named("_publisher_isni")).has_text(isni)

    def _select_contributors_tab(self):
        self.pause(self.TAB_SELECTION_DELAY)
        self.tabs(named("_tabs")).select("Contributors")

    def shows_isrc(self, code):
        self.label(with_buddy(named("_isrc"))).is_showing_on_screen()
        self.lineEdit(named("_isrc")).has_text(code)

    def change_isrc(self, code):
        self.lineEdit(named("_isrc")).change_text(code)

    def change_iswc(self, code):
        self.lineEdit(named("_iswc")).change_text(code)

    def shows_iswc(self, code):
        self.label(with_buddy(named("_iswc"))).is_showing_on_screen()
        edit = self.lineEdit(named("_iswc"))
        edit.has_text(code)

    def shows_tags(self, tags):
        self.label(with_buddy(named("_tags"))).is_showing_on_screen()
        self.lineEdit(named("_tags")).has_text(tags)

    def change_tags(self, tags):
        self.lineEdit(named("_tags")).change_text(tags)

    def shows_lyrics(self, lyrics):
        self._select_lyrics_tab()
        self.label(with_buddy(named("_lyrics"))).is_showing_on_screen()
        self.textEdit(named("_lyrics")).has_plain_text(lyrics)

    def change_lyrics(self, *lyrics):
        self._select_lyrics_tab()
        edit = self.textEdit(named("_lyrics"))
        edit.clear_all_text()
        for lyric in lyrics:
            edit.add_line(lyric)
        edit.perform(gestures.tab())

    def shows_language(self, lang):
        self._select_lyrics_tab()
        self.label(with_buddy(named("_language"))).is_showing_on_screen()
        self.combobox(named("_language")).has_current_text(lang)

    def _select_lyrics_tab(self):
        self.pause(self.TAB_SELECTION_DELAY)
        self.tabs(named("_tabs")).select("Lyrics")

    def change_language(self, lang):
        self._select_lyrics_tab()
        self.combobox(named("_language")).change_text(lang)

    def select_language(self, lang):
        self._select_lyrics_tab()
        self.combobox(named("_language")).select_option(lang)

    def shows_bitrate(self, text):
        self.label(named("_bitrate")).has_text(text)

    def shows_duration(self, text):
        self.label(named("_duration")).has_text(text)

    def shows_software_notice(self, notice):
        label = self.label(named("_software_notice"))
        label.is_showing_on_screen()
        label.has_text(notice)

    def shows_recording_studio(self, studios):
        self._select_recording_tab()
        self.label(with_buddy(named("_recording_studio"))).is_showing_on_screen()
        self.lineEdit(named("_recording_studio")).has_text(studios)

    def _select_recording_tab(self):
        self.pause(self.TAB_SELECTION_DELAY)
        self.tabs(named("_tabs")).select("Recording")

    def change_recording_studio(self, studios):
        self._select_recording_tab()
        self.lineEdit(named("_recording_studio")).change_text(studios)

    def shows_recording_studio_region(self, name):
        self._select_recording_tab()
        self.label(with_buddy(named("_recording_studio_region"))).is_showing_on_screen()
        edit = self.lineEdit(named("_recording_studio_region"))
        edit.has_text(name)

    def change_recording_studio_region(self, name):
        self._select_recording_tab()
        self.lineEdit(named("_recording_studio_region")).change_text(name)

    def shows_recording_studio_address(self, address):
        self._select_recording_tab()
        self.label(with_buddy(named("_recording_studio_address"))).is_showing_on_screen()
        edit = self.lineEdit(named("_recording_studio_address"))
        edit.has_text(address)

    def change_recording_studio_address(self, address):
        self._select_recording_tab()
        self.lineEdit(named("_recording_studio_address")).change_text(address)

    def shows_production_company(self, producer):
        self._select_recording_tab()
        self.label(with_buddy(named("_production_company"))).is_showing_on_screen()
        self.lineEdit(named("_production_company")).has_text(producer)

    def change_production_company(self, producer):
        self._select_recording_tab()
        self.lineEdit(named("_production_company")).change_text(producer)

    def shows_production_company_region(self, name):
        self._select_recording_tab()
        self.label(with_buddy(named("_production_company_region"))).is_showing_on_screen()
        edit = self.lineEdit(named("_production_company_region"))
        edit.has_text(name)

    def change_production_company_region(self, name):
        self._select_recording_tab()
        self.lineEdit(named("_production_company_region")).change_text(name)

    def shows_music_producer(self, producer):
        self._select_recording_tab()
        self.label(with_buddy(named("_music_producer"))).is_showing_on_screen()
        self.lineEdit(named("_music_producer")).has_text(producer)

    def change_music_producer(self, producer):
        self._select_recording_tab()
        self.lineEdit(named("_music_producer")).change_text(producer)

    def shows_mixer(self, mixer):
        self._select_recording_tab()
        self.label(with_buddy(named("_mixer"))).is_showing_on_screen()
        self.lineEdit(named("_mixer")).has_text(mixer)

    def change_mixer(self, mixer):
        self._select_recording_tab()
        self.lineEdit(named("_mixer")).change_text(mixer)

    def shows_primary_style(self, style):
        self.label(with_buddy(named("_genre"))).is_showing_on_screen()
        self.combobox(named("_genre")).has_current_text(style)

    def change_primary_style(self, style):
        self.combobox(named("_genre")).change_text(style)

    def select_primary_style(self, style):
        self.combobox(named("_genre")).select_option(style)

    def shows_recording_time(self, time):
        self._select_recording_tab()
        self.label(with_buddy(named("_recording_time"))).is_showing_on_screen()
        self.dateEdit(named("_recording_time")).has_date(time)

    def change_recording_time(self, year, month, day):
        self._select_recording_tab()
        self.dateEdit(named("_recording_time")).enter_date(year, month, day)
