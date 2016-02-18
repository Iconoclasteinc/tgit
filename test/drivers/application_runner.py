# -*- coding: utf-8 -*-
import sip
from collections import namedtuple
from traceback import format_exception
import sys

from cute.animatron import Animatron
from cute.matchers import named, showing_on_screen
from cute.prober import EventProcessingProber
from cute.widgets import main_application_window
from test.drivers import track_selection_dialog, message_box
from test.util.doubles import fake_audio_player
from tgit import platforms
from tgit.cheddar import Cheddar
from tgit.tagger import TGiT
from .main_window_driver import MainWindowDriver


def _print_unhandled_exceptions():
    def exception_hook(exctype, value, traceback):
        for line in format_exception(exctype, value, traceback):
            print(line, file=sys.stderr)

    sys.excepthook = exception_hook


def _make_tracks(tracks):
    Track = namedtuple("Track", "title")
    return map(Track._make, tracks)


class ApplicationRunner:
    STARTUP_DELAY = 250 if platforms.mac else 0
    DRAG_AND_DROP_DELAY = 100
    SAVE_DELAY = 500

    app = None
    tagger = None

    def __init__(self, workspace, settings):
        self._workspace = workspace
        self._settings = settings

    def start(self):
        _print_unhandled_exceptions()
        self.app = TGiT(fake_audio_player, Cheddar(host="localhost", port=5001, secure=False),
                        self._settings, native=False, confirm_exit=False)

        self.app.show()
        self.tagger = MainWindowDriver(main_application_window(named("main_window"), showing_on_screen()),
                                       EventProcessingProber(timeout_in_ms=1000), Animatron())
        self.tagger.pause(self.STARTUP_DELAY)

    def stop(self):
        self.tagger.close()
        self.app.quit()
        # If we don't force deletion of the C++ wrapped object, it causes the test suite to eventually crash
        # Never ever remove this!!
        sip.delete(self.app)

    def new_project(self, name="album", of_type="mp3"):
        self.tagger.create_project(of_type, name, self._workspace.root_path)

    def add_tracks_to_project(self, *tracks):
        self.tagger.add_tracks_to_project()
        track_selection_dialog(self.tagger).select_tracks(*tracks)

    def import_project(self, name, from_track, of_type="mp3"):
        self.tagger.create_project(of_type=of_type, name=name, location=self._workspace.root_path,
                                   import_from=from_track)

    def shows_track_list(self, *tracks):
        self.tagger.navigate_to_track_list_page()
        self.tagger.shows_project_contains(*tracks)

    def change_order_of_tracks(self, *tracks):
        for position, track in enumerate(_make_tracks(tracks)):
            self.tagger.move_track(track.title, position)
            self.tagger.pause(self.DRAG_AND_DROP_DELAY)

    def remove_track(self, title):
        self.tagger.remove_track(title)

    def shows_project_metadata(self, **tags):
        self.tagger.navigate_to_project_page()
        self.tagger.shows_project_metadata(**tags)

    def change_project_metadata(self, **tags):
        self.tagger.edit_project_metadata(**tags)

    def shows_next_track_metadata(self, **tags):
        self.tagger.next()
        self.tagger.shows_track_metadata(**tags)

    def shows_track_metadata(self, track_number, track_title, **tags):
        self.tagger.navigate_to_track_page(track_title, track_number)
        self.tagger.shows_track_metadata(track_number=track_number, track_title=track_title, **tags)

    def change_track_metadata(self, **tags):
        self.tagger.edit_track_metadata(**tags)

    def change_track_position(self, title, to_position):
        self.tagger.move_track(title, to_position - 1)

    def change_settings(self, **settings):
        self.tagger.change_settings(**settings)

    def has_settings(self, **settings):
        self.tagger.has_settings(**settings)

    def assign_isni_to_main_artist(self):
        self.tagger.assign_isni_to_main_artist()
        # todo remove and verify in test that album metadata shows the isni
        self.tagger.pause(100)

    def save_project(self):
        self.tagger.save()
        self.tagger.pause(self.SAVE_DELAY)

    def find_isni_of_main_artist(self):
        self.tagger.find_isni_of_main_artist()
        # todo remove and verify in test that album metadata shows the isni
        self.tagger.pause(100)

    def close_project(self):
        self.tagger.close_project()
        self.tagger.pause(100)
        message_box(self.tagger).click_yes()
        self.tagger.shows_welcome_screen()

    def load_project(self, album_name):
        self.tagger.load_project(self._workspace.file(album_name, album_name + ".tgit"))

    def save(self):
        self.tagger.save()

    def sign_in(self):
        self.sign_in_as("test@example.com")

    def sign_in_as(self, email):
        self.tagger.sign_in_as(email, "passw0rd")
        self.tagger.is_signed_in_as(email)

    def sign_out(self):
        self.tagger.sign_out()
        self.tagger.is_signed_out()

    def is_signed_in_as(self, email):
        self.tagger.is_signed_in_as(email)

    def is_signed_out(self):
        self.tagger.is_signed_out()

    def declare_project_to_soproq(self, filename):
        self.tagger.declare_project_to_soproq(self._workspace.file(filename))
