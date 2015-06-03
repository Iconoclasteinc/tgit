# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from hamcrest.library.text import contains_string

from cute.matchers import named
from tgit.ui.album_screen import AlbumScreen
from ._screen_driver import ScreenDriver
from .album_edition_page_driver import album_edition_page
from .album_composition_page_driver import album_composition_page
from .track_edition_page_driver import track_edition_page
from .track_selection_dialog_driver import track_selection_dialog


def album_screen(parent):
    return AlbumScreenDriver.find_single(parent, AlbumScreen, named("album_screen"))


class AlbumScreenDriver(ScreenDriver):
    def showsAlbumCompositionPage(self):
        album_composition_page(self).is_showing_on_screen()

    def showsAlbumEditionPage(self):
        album_edition_page(self).is_showing_on_screen()

    def showsTrackEditionPage(self):
        track_edition_page(self).is_showing_on_screen()

    def add_tracks_to_album(self, *paths):
        album_composition_page(self).add_tracks()
        track_selection_dialog(self).select_tracks(*paths)

    def remove_track(self, title):
        album_composition_page(self).remove_track(title)

    def move_track(self, title, to):
        album_composition_page(self).move_track_in_bottom_table(title, to)

    def previousPage(self):
        self.button(named("previous")).click()

    def nextPage(self):
        self.button(named("next")).click()

    def save(self):
        self.button(named("save")).click()

    def hidesPreviousPageButton(self):
        self._is_disabled(self.button(named("previous")))

    def showsPreviousPageButton(self):
        self._is_enabled(self.button(named("previous")))

    def hidesNextPageButton(self):
        self._is_disabled(self.button(named("next")))

    def showsNextPageButton(self):
        self._is_enabled(self.button(named("next")))

    def hidesSaveButton(self):
        self._is_disabled(self.button(named("save")))

    def showsSaveButton(self):
        self._is_enabled(self.button(named("save")))

    def shows_album_contains(self, *tracks):
        album_composition_page(self).showsTracksInOrder(*tracks)

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

    @staticmethod
    def _is_disabled(button):
        button.is_disabled()
        button.has_cursor_shape(Qt.ArrowCursor)

    @staticmethod
    def _is_enabled(button):
        button.is_enabled()
        button.has_cursor_shape(Qt.PointingHandCursor)