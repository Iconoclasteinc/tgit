# -*- coding: utf-8 -*-
from hamcrest.library.text import contains_string

from cute.matchers import named
from tgit.ui.album_screen import AlbumScreen
from ._screen_driver import ScreenDriver
from .album_edition_page_driver import album_edition_page, no_album_edition_page
from .track_list_page_driver import track_list_page, no_track_list_page
from .track_edition_page_driver import track_edition_page, no_track_edition_page


def album_screen(parent):
    return AlbumScreenDriver.find_single(parent, AlbumScreen, named("album_screen"))


class AlbumScreenDriver(ScreenDriver):
    def shows_track_list_page(self):
        track_list_page(self).is_showing_on_screen()

    def has_no_track_list_page(self):
        no_track_list_page(self).exists()

    def shows_album_edition_page(self):
        album_edition_page(self).is_showing_on_screen()

    def has_no_album_edition_page(self):
        no_album_edition_page(self).exists()

    def shows_track_edition_page(self):
        page = track_edition_page(self)
        page.is_showing_on_screen()
        return page

    def has_no_track_edition_page(self):
        no_track_edition_page(self).exists()

    def add_tracks_to_album(self):
        track_list_page(self).add_tracks()

    def remove_track(self, title):
        track_list_page(self).remove_track(title)

    def move_track(self, title, to):
        track_list_page(self).move_track(title, to)

    def to_previous_page(self):
        self.button(named("previous")).click()

    def to_next_page(self):
        self.button(named("next")).click()

    def is_missing_previous_page_button(self):
        self.button(named("previous")).is_disabled()

    def is_missing_next_page_button(self):
        self.button(named("next")).is_disabled()

    def shows_album_contains(self, *tracks):
        track_list_page(self).shows_tracks_in_order(*tracks)

    def shows_album_metadata(self, **tags):
        album_edition_page(self).shows_metadata(**tags)

    def edit_album_metadata(self, **tags):
        album_edition_page(self).change_metadata(**tags)

    def shows_track_metadata(self, **tags):
        track_edition_page(self).shows_metadata(**tags)

    def edit_track_metadata(self, **tags):
        track_edition_page(self).change_metadata(**tags)

    def links_help_to(self, location):
        self.label(named("help_link")).has_text(contains_string("href=\"{0}\"".format(location)))

    def links_feature_request_to(self, location):
        self.label(named("feature_request_link")).has_text(contains_string("href=\"{0}".format(location)))

    def assign_isni_to_lead_performer(self):
        album_edition_page(self).assign_isni_to_lead_performer()

    def lookup_isni_of_lead_performer(self):
        album_edition_page(self).lookup_isni_of_lead_performer()

    def lookup_isni_is_enabled(self, enabled=True):
        album_edition_page(self).enables_isni_lookup(enabled=enabled)
