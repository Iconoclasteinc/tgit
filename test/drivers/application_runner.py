# -*- coding: utf-8 -*-
from collections import namedtuple
import sip

from cute.animatron import Animatron
from tgit.isni.name_registry import NameRegistry
from cute.matchers import named, showing_on_screen
from cute.widgets import main_application_window
from cute.prober import EventProcessingProber
from test.util import doubles
from tgit.tagger import TGiT
from .main_window_driver import MainWindowDriver

ONE_SECOND_IN_MILLISECONDS = 1000
SAVE_DELAY = 500


def _make_tracks(tracks):
    Track = namedtuple("Track", "title")
    return map(Track._make, tracks)


class ApplicationRunner:
    app = None
    tagger = None

    def __init__(self, workspace):
        self._workspace = workspace

    def start(self, preferences):
        self.app = TGiT(doubles.audio_player(), NameRegistry(host="localhost", assign_host="localhost", port=5000),
                        use_local_isni_backend=True, native=False)
        self.app.show(preferences)
        self.tagger = MainWindowDriver(main_application_window(named("main_window"), showing_on_screen()),
                                       EventProcessingProber(timeout_in_ms=ONE_SECOND_IN_MILLISECONDS), Animatron())

    def stop(self):
        self.tagger.close()
        self.app.quit()
        # If we don't force deletion of the C++ wrapped object, it causes the test suite to eventually crash
        # Never ever remove this!!
        sip.delete(self.app)

    def new_album(self, of_type="mp3", filename="album"):
        self.tagger.create_album(of_type, filename, self._workspace.root_path)

    def add_tracks_to_album(self, *tracks):
        self.tagger.add_tracks_to_album(*tracks)

    def import_album(self, from_track, of_type="mp3", save_as="album"):
        self.tagger.import_album(of_type=of_type, name=save_as, track_path=from_track,
                                 album_path=self._workspace.root_path)

    def shows_album_content(self, *tracks):
        self.tagger.shows_album_contains(*tracks)

    def change_order_of_tracks(self, *tracks):
        for position, track in enumerate(_make_tracks(tracks)):
            self.tagger.move_track(track.title, position)
            self.tagger.pause(100)

    def remove_track(self, title):
        self.tagger.remove_track(title)

    def shows_album_metadata(self, **tags):
        self.tagger.next()
        self.tagger.shows_album_metadata(**tags)
        # todo navigate back to track list
        # so we always no where we're starting from

    def change_album_metadata(self, **tags):
        self.tagger.edit_album_metadata(**tags)

    def shows_next_track_metadata(self, **tags):
        self.tagger.next()
        self.tagger.shows_track_metadata(**tags)

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

    def save_album(self):
        self.tagger.save()
        self.tagger.pause(SAVE_DELAY)

    def fails_to_assign_isni_to_lead_performer(self):
        self.tagger.assign_isni_to_lead_performer()
        self.tagger.shows_assignation_failed()

    def find_isni_of_lead_performer(self):
        self.tagger.find_isni_of_lead_performer()

    def close_album(self):
        self.tagger.close_album()
        self.tagger.shows_confirmation_message()
        self.tagger.shows_welcome_screen()

    def load_album(self, album_name):
        self.tagger.load_album(self._workspace.file(album_name))

    def save(self):
        self.tagger.save()
