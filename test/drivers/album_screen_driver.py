# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from hamcrest.library.text import contains_string

from cute.matchers import named
from test.drivers import ScreenDriver, track_selection_dialog
from test.drivers.album_edition_page_driver import album_edition_page
from test.drivers.album_composition_page_driver import album_composition_page
from test.drivers.track_edition_page_driver import track_edition_page
from tgit.ui.album_screen import AlbumScreen


def album_screen(parent):
    return AlbumScreenDriver.find_single(parent, AlbumScreen, named('album-screen'))


class AlbumScreenDriver(ScreenDriver):
    def showsAlbumCompositionPage(self):
        album_composition_page(self).is_showing_on_screen()

    def showsAlbumEditionPage(self):
        album_edition_page(self).is_showing_on_screen()

    def showsTrackEditionPage(self):
        track_edition_page(self).is_showing_on_screen()

    def add_tracks_to_album(self, *paths, of_type):
        album_composition_page(self).add_tracks()
        track_selection_dialog(self).select_tracks(*paths, of_type=of_type)

    def removeTrack(self, title):
        album_composition_page(self).removeTrack(title)

    def moveTrack(self, title, to):
        album_composition_page(self).moveTrack(title, to)

    def previousPage(self):
        self.button(named('previous')).click()

    def nextPage(self):
        self.button(named('next')).click()

    def save(self):
        self.button(named('save')).click()

    def hidesPreviousPageButton(self):
        self._is_disabled(self.button(named('previous')))

    def showsPreviousPageButton(self):
        self._is_enabled(self.button(named('previous')))

    def hidesNextPageButton(self):
        self._is_disabled(self.button(named('next')))

    def showsNextPageButton(self):
        self._is_enabled(self.button(named('next')))

    def hidesSaveButton(self):
        self._is_disabled(self.button(named('save')))

    def showsSaveButton(self):
        self._is_enabled(self.button(named('save')))

    def showsAlbumContains(self, *tracks):
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
        self.label(named('help-link')).has_text(contains_string('href="%s"' % location))

    def linksFeatureRequestTo(self, location):
        self.label(named('feature-request-link')).has_text(contains_string('href="%s' % location))

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