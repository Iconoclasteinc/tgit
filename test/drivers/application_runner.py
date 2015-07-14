# -*- coding: utf-8 -*-
from collections import namedtuple
import sip

from cute.animatron import Animatron
from test.drivers import track_selection_dialog, message_box
from test.util.doubles import fake_audio_player
from tgit.isni.name_registry import NameRegistry
from cute.matchers import named, showing_on_screen
from cute.widgets import main_application_window
from cute.prober import EventProcessingProber
from tgit.tagger import TGiT
from .main_window_driver import MainWindowDriver


ignore = lambda *_: None


def _make_tracks(tracks):
    Track = namedtuple("Track", "title")
    return map(Track._make, tracks)


class ApplicationRunner:
    DRAG_AND_DROP_DELAY = 100
    SAVE_DELAY = 500

    app = None
    tagger = None

    def __init__(self, workspace):
        self._workspace = workspace

    def start(self, preferences):
        self.app = TGiT(fake_audio_player, ignore, NameRegistry(host="localhost", assign_host="localhost", port=5000),
                        use_local_isni_backend=True, native=False, confirm_exit=False)
        self.app.show(preferences)
        self.tagger = MainWindowDriver(main_application_window(named("main_window"), showing_on_screen()),
                                       EventProcessingProber(timeout_in_ms=1000), Animatron())

    def stop(self):
        self.tagger.close()
        self.app.quit()
        # If we don't force deletion of the C++ wrapped object, it causes the test suite to eventually crash
        # Never ever remove this!!
        sip.delete(self.app)

    def new_album(self, name="album", of_type="mp3"):
        self.tagger.create_album(of_type, name, self._workspace.root_path)

    def add_tracks_to_album(self, *tracks):
        self.tagger.add_tracks_to_album()
        track_selection_dialog(self.tagger).select_tracks(*tracks)

    def import_album(self, name, from_track, of_type="mp3"):
        self.tagger.create_album(of_type=of_type, name=name, location=self._workspace.root_path,
                                 import_from=from_track)

    def shows_track_list(self, *tracks):
        self.tagger.navigate_to_track_list_page()
        self.tagger.shows_album_contains(*tracks)

    def change_order_of_tracks(self, *tracks):
        for position, track in enumerate(_make_tracks(tracks)):
            self.tagger.move_track(track.title, position)
            self.tagger.pause(self.DRAG_AND_DROP_DELAY)

    def remove_track(self, title):
        self.tagger.remove_track(title)

    def shows_album_metadata(self, **tags):
        self.tagger.navigate_to_album_page()
        self.tagger.shows_album_metadata(**tags)

    def change_album_metadata(self, **tags):
        self.tagger.edit_album_metadata(**tags)

    def shows_next_track_metadata(self, **tags):
        self.tagger.next()
        self.tagger.shows_track_metadata(**tags)

    def shows_track_metadata(self, track_number, track_title, **tags):
        self.tagger.navigate_to_track_page(track_title, track_number)
        self.tagger.shows_track_metadata(track_number=track_number, track_title=track_title, **tags)

    def change_track_metadata(self, **tags):
        self.tagger.editTrackMetadata(**tags)

    def change_track_position(self, title, to_position):
        self.tagger.move_track(title, to_position - 1)

    def change_settings(self, **settings):
        self.tagger.change_settings(**settings)

    def has_settings(self, **settings):
        self.tagger.has_settings(**settings)

    def assign_isni_to_lead_performer(self):
        self.tagger.assign_isni_to_lead_performer()
        # todo remove and verify in test that album metadata shows the isni
        self.tagger.pause(100)

    def save_album(self):
        self.tagger.save()
        self.tagger.pause(self.SAVE_DELAY)

    def fails_to_assign_isni_to_lead_performer(self):
        self.tagger.assign_isni_to_lead_performer()
        self.tagger.shows_assignation_failed()

    def find_isni_of_lead_performer(self):
        self.tagger.find_isni_of_lead_performer()
        # todo remove and verify in test that album metadata shows the isni
        self.tagger.pause(100)

    def close_album(self):
        self.tagger.close_album()
        message_box(self.tagger).yes()
        self.tagger.shows_welcome_screen()

    def load_album(self, album_name):
        self.tagger.load_album(self._workspace.file(album_name, album_name + ".tgit"))

    def save(self):
        self.tagger.save()
