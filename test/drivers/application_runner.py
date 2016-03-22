# -*- coding: utf-8 -*-
from collections import namedtuple

from cute.animatron import Animatron
from cute.matchers import named, showing_on_screen
from cute.prober import EventProcessingProber
from cute.widgets import main_application_window
from test.drivers import track_selection_dialog, message_box
from test.util.doubles import fake_audio_player
from tgit import platforms
from tgit.album_portfolio import AlbumPortfolio
from tgit.cheddar import Cheddar
from .main_window_driver import MainWindowDriver
from tgit.tagger import Tagger


def _make_tracks(tracks):
    Track = namedtuple("Track", "title")
    return map(Track._make, tracks)


class ApplicationRunner:
    STARTUP_DELAY = 250 if platforms.mac else 0
    DRAG_AND_DROP_DELAY = 100 if platforms.mac else 0
    SAVE_DELAY = 500 if platforms.mac else 0

    main_window_driver = None

    def __init__(self, workspace, settings):
        self._workspace = workspace
        self._settings = settings

    def start(self):
        Tagger(self._settings.load_session(), AlbumPortfolio(), fake_audio_player(),
               Cheddar(host="localhost", port=5001, secure=False), self._settings.load_user_preferences(),
               native=False, confirm_exit=False).show()

        self.main_window_driver = MainWindowDriver(main_application_window(named("main_window"), showing_on_screen()),
                                                   EventProcessingProber(timeout_in_ms=1000), Animatron())
        self.main_window_driver.pause(self.STARTUP_DELAY)

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
        self.main_window_driver.navigate_to_project_page()
        self.main_window_driver.shows_project_contains(*tracks)

    def change_order_of_tracks(self, *tracks):
        for position, track in enumerate(_make_tracks(tracks)):
            self.main_window_driver.move_track(track.title, position)
            self.main_window_driver.pause(self.DRAG_AND_DROP_DELAY)

    def remove_track(self, title):
        self.main_window_driver.remove_track(title)

    def shows_project_metadata(self, **tags):
        self.main_window_driver.navigate_to_project_page()
        self.main_window_driver.shows_project_metadata(**tags)

    def change_project_metadata(self, **tags):
        self.main_window_driver.edit_project_metadata(**tags)

    def shows_next_track_metadata(self, **tags):
        self.main_window_driver.next()
        self.main_window_driver.shows_track_metadata(**tags)

    def shows_track_metadata(self, track_number, track_title, **tags):
        self.main_window_driver.navigate_to_track_page(track_title, track_number)
        self.main_window_driver.shows_track_metadata(track_number=track_number, track_title=track_title, **tags)

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
        # todo remove and verify in test that album metadata shows the isni
        self.main_window_driver.pause(100)

    def save_project(self):
        self.main_window_driver.save()
        self.main_window_driver.pause(self.SAVE_DELAY)

    def find_isni_of_main_artist(self, name):
        self.main_window_driver.find_isni_of_main_artist(name)
        # todo remove and verify in test that album metadata shows the isni
        self.main_window_driver.pause(100)

    def close_project(self):
        self.main_window_driver.close_project()
        self.main_window_driver.pause(100)
        message_box(self.main_window_driver).click_yes()
        self.main_window_driver.shows_welcome_screen()

    def load_project(self, album_name):
        self.main_window_driver.load_project(self._workspace.file(album_name, album_name + ".tgit"))

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
