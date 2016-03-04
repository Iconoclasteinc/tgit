# -*- coding: utf-8 -*-
from hamcrest.library.text import contains_string

from cute import gestures
from cute.matchers import named
from tgit.ui.pages.project_screen import ProjectScreen
from ._screen_driver import ScreenDriver
from .project_edition_page_driver import project_edition_page, no_project_edition_page
from .track_list_tab_driver import track_list_tab
from .track_edition_page_driver import track_edition_page, no_track_edition_page


def project_screen(parent):
    return ProjectScreenDriver.find_single(parent, ProjectScreen, named("project_screen"))


class ProjectScreenDriver(ScreenDriver):
    def shows_pages_in_navigation_combo(self, *pages):
        self.combobox(named("_pages_navigation")).has_options(*pages)

    def shows_project_edition_page(self):
        project_edition_page(self).is_showing_on_screen()

    def has_no_project_edition_page(self):
        no_project_edition_page(self).exists()

    def shows_track_edition_page(self, number):
        track_edition_page(self, number).is_showing_on_screen()

    def has_no_track_edition_page(self):
        no_track_edition_page(self).exists()

    def add_tracks_to_project(self):
        track_list_tab(self).add_tracks()

    def remove_track(self, title):
        track_list_tab(self).remove_track(title)

    def move_track(self, title, to):
        track_list_tab(self).move_track(title, to)

    def to_previous_page(self):
        self.button(named("_previous")).click()

    def to_next_page(self):
        self.button(named("_next")).click()

    def to_page(self, name):
        self.combobox(named("_pages_navigation")).select_option(name)

    def shows_page_in_navigation_combo(self, name):
        self.combobox(named("_pages_navigation")).has_current_text(name)

    def does_not_show_page_in_navigation_combo(self, name):
        self.combobox(named("_pages_navigation")).has_not_option(name)

    def shows_previous_page_button(self, enabled=True):
        self.button(named("_previous")).is_enabled(enabled)

    def shows_next_page_button(self, enabled=True):
        self.button(named("_next")).is_enabled(enabled)

    def shows_project_contains(self, *tracks):
        track_list_tab(self).shows_tracks_in_order(*tracks)

    def shows_project_metadata(self, **tags):
        project_edition_page(self).shows_metadata(**tags)

    def edit_project_metadata(self, **tags):
        project_edition_page(self).change_metadata(**tags)

    def shows_track_metadata(self, **tags):
        track_edition_page(self).shows_metadata(**tags)

    def edit_track_metadata(self, **tags):
        track_edition_page(self).change_metadata(**tags)

    def links_help_to(self, location):
        self.label(named("help_link")).has_text(contains_string("href=\"{0}\"".format(location)))

    def links_feature_request_to(self, location):
        self.label(named("feature_request_link")).has_text(contains_string("href=\"{0}".format(location)))

    def assign_isni_to_main_artist(self):
        project_edition_page(self).assign_isni_to_main_artist()

    def lookup_isni_of_main_artist(self):
        project_edition_page(self).lookup_isni_of_main_artist()

    def lookup_isni_is_enabled(self, enabled=True):
        project_edition_page(self).shows_main_artist_isni_lookup_button(enabled=enabled)

    def quick_navigate_to_page(self, text):
        self.click()
        self.perform(gestures.quick_nav())
        self.perform(gestures.type_text(text))
        self.enter()
