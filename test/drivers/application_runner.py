# -*- coding: utf-8 -*-
from collections import namedtuple

from tgit.isni.name_registry import NameRegistry
from cute.matchers import named, showing_on_screen
from cute.widgets import main_application_window
from cute.prober import EventProcessingProber
from cute.robot import Robot
from test.util import doubles
from tgit.tagger import TGiT
from .main_window_driver import MainWindowDriver

ONE_SECOND_IN_MILLISECONDS = 1000


def _make_tracks(tracks):
    Track = namedtuple('Track', 'title')
    return map(Track._make, tracks)


class ApplicationRunner:
    app = None
    tagger = None

    def start(self, preferences):
        self.app = TGiT(doubles.audio_player(), NameRegistry(host="localhost", assign_host="localhost", port=5000),
                        use_local_isni_backend=True, native=False)
        self.app.show(preferences)
        self.tagger = MainWindowDriver(main_application_window(named("main_window"), showing_on_screen()),
                                       EventProcessingProber(timeout_in_ms=ONE_SECOND_IN_MILLISECONDS), Robot())

    def stop(self):
        self.tagger.close()
        del self.tagger
        self.app.quit()
        del self.app

    def new_album(self, of_type="mp3"):
        self.tagger.create_album(of_type)

    def add_tracks_to_album(self, *tracks):
        self.tagger.add_tracks_to_album(*tracks)

    def import_album(self, track, of_type="mp3"):
        self.tagger.import_album(track, of_type=of_type)

    def shows_album_content(self, *tracks):
        self.tagger.shows_album_contains(*tracks)

    def change_order_of_tracks(self, *tracks):
        for position, track in enumerate(_make_tracks(tracks)):
            self.tagger.move_track(track.title, position)

    def remove_tracks(self, *titles):
        for title in titles:
            self.tagger.remove_track(title)

    def shows_album_metadata(self, **tags):
        self.tagger.next()
        self.tagger.shows_album_metadata(**tags)
        # todo navigate back to track list
        # so we always no where we're starting from

    def change_album_metadata(self, **tags):
        self.tagger.edit_album_metadata(**tags)
        self.tagger.save_album()

    def shows_next_track_metadata(self, **tags):
        self.tagger.next()
        self.tagger.shows_track_metadata(**tags)

    def change_track_metadata(self, **tags):
        self.tagger.editTrackMetadata(**tags)
        self.tagger.save_album()

    def change_track_position(self, title, to_position):
        self.tagger.move_track(title, to_position - 1)

    def change_settings(self, **settings):
        self.tagger.change_settings(**settings)

    def has_settings(self, **settings):
        self.tagger.has_settings(**settings)

    def assign_isni_to_lead_performer(self):
        self.tagger.assign_isni_to_lead_performer()
        self.tagger.save_album()

    def tries_to_assign_isni_to_lead_performer_with_invalid_data(self):
        self.tagger.tries_to_assign_isni_to_lead_performer_with_invalid_data()

    def finds_isni_of_lead_performer(self):
        self.tagger.finds_isni_of_lead_performer()
        self.tagger.save_album()

    def closes_album(self):
        self.tagger.closes_album()