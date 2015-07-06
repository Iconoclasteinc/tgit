# -*- coding: utf-8 -*-
from hamcrest.library.text import contains_string

from cute.matchers import named
from tgit.ui.album_screen import AlbumScreen
from ._screen_driver import ScreenDriver
from .album_edition_page_driver import album_edition_page
from .track_list_page_driver import track_list_page
from .track_edition_page_driver import track_edition_page


def album_screen(parent):
    return AlbumScreenDriver.find_single(parent, AlbumScreen, named("album_screen"))


class AlbumScreenDriver(ScreenDriver):
    def shows_track_list_page(self):
        track_list_page(self).is_showing_on_screen()

    def showsAlbumEditionPage(self):
        album_edition_page(self).is_showing_on_screen()

    def showsTrackEditionPage(self):
        track_edition_page(self).is_showing_on_screen()

    def add_tracks_to_album(self):
        track_list_page(self).add_tracks()

    def remove_track(self, title):
        track_list_page(self).remove_track(title)

    def move_track(self, title, to):
        track_list_page(self).move_track(title, to)

    def previousPage(self):
        self.button(named("previous")).click()

    def nextPage(self):
        self.button(named("next")).click()

    def hidesPreviousPageButton(self):
        self.button(named("previous")).is_disabled()

    def showsPreviousPageButton(self):
        self.button(named("previous")).is_enabled()

    def hidesNextPageButton(self):
        self.button(named("next")).is_disabled()

    def showsNextPageButton(self):
        self.button(named("next")).is_enabled()

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

    def linksHelpTo(self, location):
        self.label(named("help_link")).has_text(contains_string("href=\"{0}\"".format(location)))

    def linksFeatureRequestTo(self, location):
        self.label(named("feature_request_link")).has_text(contains_string("href=\"{0}".format(location)))

    def assign_isni_to_lead_performer(self):
        album_edition_page(self).assign_isni_to_lead_performer()

    def lookup_isni_of_lead_performer(self):
        album_edition_page(self).lookup_isni_of_lead_performer()
