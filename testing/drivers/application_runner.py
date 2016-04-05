# -*- coding: utf-8 -*-
from collections import namedtuple

from hamcrest import starts_with

from cute.animatron import Animatron
from cute.matchers import named, showing_on_screen
from cute.prober import EventProcessingProber
from cute.widgets import main_application_window
from testing.doubles import fake_audio_player
from tgit import platforms
from tgit.cheddar import Cheddar
from tgit.project_studio import ProjectStudio
from tgit.tagger import Tagger
from .main_window_driver import MainWindowDriver
from .message_box_driver import message_box
from .track_selection_dialog_driver import track_selection_dialog


def _make_tracks(tracks):
    Track = namedtuple("Track", "title")
    return map(Track._make, tracks)


class ApplicationRunner:
    MESSAGE_BOX_DISPLAY_DELAY = 100 if platforms.mac else 0
    SAVE_DELAY = 250 if platforms.mac else 0

    main_window_driver = None

    def __init__(self, workspace, settings):
        self._workspace = workspace
        self._settings = settings

    def start(self):
        Tagger(self._settings, ProjectStudio(), fake_audio_player(),
               Cheddar(host="127.0.0.1", port=5001, secure=False),
               native=False, confirm_exit=False).show()

        self.main_window_driver = MainWindowDriver(main_application_window(named("main_window"), showing_on_screen()),
                                                   EventProcessingProber(timeout_in_ms=2000), Animatron())

    def stop(self):
        self.main_window_driver.close()

    def new_project(self, name="album", of_type="mp3"):
        self.main_window_driver.create_project(of_type, name, self._workspace.root_path)

    def add_tracks_to_project(self, *tracks):
        self.main_window_driver.add_tracks_to_project()
        track_selection_dialog(self.main_window_driver).select_tracks(*tracks)

    def import_project(self, name, from_track, of_type="mp3"):
        self.main_window_driver.create_project(of_type=of_type, name=name, location=self._workspace.root_path,
                                               import_from=from_track)

    def shows_track_list(self, *tracks):
        self.main_window_driver.shows_project_contains(*tracks)

    def change_order_of_tracks(self, *tracks):
        for position, track in enumerate(_make_tracks(tracks)):
            self.main_window_driver.move_track(track.title, position)

    def remove_track(self, title):
        self.main_window_driver.remove_track(title)

    def shows_project_metadata(self, **tags):
        self.main_window_driver.shows_project_metadata(**tags)

    def navigate_to_project_page(self):
        self.main_window_driver.navigate_to_project_page()

    def change_project_metadata(self, **tags):
        self.main_window_driver.edit_project_metadata(**tags)

    def shows_next_track_metadata(self, **tags):
        self.main_window_driver.next()
        self.main_window_driver.shows_track_metadata(**tags)

    def shows_track_metadata(self, track_number, track_title, **tags):
        self.navigate_to_track_page(track_number, track_title)
        self.main_window_driver.shows_track_metadata(track_number=track_number, track_title=track_title, **tags)

    def navigate_to_track_page(self, track_number, track_title):
        self.main_window_driver.navigate_to_track_page(track_title, track_number)

    def change_track_metadata(self, **tags):
        self.main_window_driver.edit_track_metadata(**tags)

    def change_track_position(self, title, to_position):
        self.main_window_driver.move_track(title, to_position - 1)

    def change_settings(self, **settings):
        self.main_window_driver.change_settings(**settings)

    def has_settings(self, **settings):
        self.main_window_driver.has_settings(**settings)

    def assign_isni_to_main_artist(self):
        self.main_window_driver.assign_isni_to_main_artist()

    def save_project(self):
        self.main_window_driver.save()
        self.main_window_driver.pause(self.SAVE_DELAY)

    def find_isni_of_main_artist(self, name):
        self.main_window_driver.find_isni_of_main_artist(name)

    def close_project(self):
        self.main_window_driver.close_project()
        self.main_window_driver.pause(self.MESSAGE_BOX_DISPLAY_DELAY)
        message_box(self.main_window_driver).click_yes()
        self.main_window_driver.shows_welcome_screen()

    def load_project(self, album_name):
        self.main_window_driver.load_project(self._project_file_path(album_name))

    def shows_recent_projects(self, *names):
        self.main_window_driver.shows_recent_projects(*(starts_with(name) for name in names))

    def open_recent_project(self, name):
        self.main_window_driver.open_recent_project(starts_with(name))

    def save(self):
        self.main_window_driver.save()

    def sign_in(self):
        self.sign_in_as("test@example.com")

    def sign_in_as(self, email):
        self.main_window_driver.sign_in_as(email, "passw0rd")
        self.main_window_driver.is_signed_in_as(email)

    def sign_out(self):
        self.main_window_driver.sign_out()
        self.main_window_driver.is_signed_out()

    def is_signed_in_as(self, email):
        self.main_window_driver.is_signed_in_as(email)

    def is_signed_out(self):
        self.main_window_driver.is_signed_out()

    def declare_project_to_soproq(self, filename):
        self.main_window_driver.declare_project_to_soproq(self._workspace.file(filename))

    def _project_file_path(self, name):
        return self._workspace.file(name, name + ".tgit")
