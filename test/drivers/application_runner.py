# -*- coding: utf-8 -*-
from tgit.isni.name_registry import NameRegistry
from test.cute.matchers import named, showingOnScreen
from test.cute.widgets import mainApplicationWindow
from test.cute.prober import EventProcessingProber
from test.cute.robot import Robot
from test.drivers.tagger_driver import TaggerDriver
from test.util import doubles
from tgit.preferences import Preferences
from tgit.tagger import TGiT

ONE_SECOND = 1000


class ApplicationRunner(object):
    def start(self, preferences=Preferences()):
        self.app = TGiT(doubles.audioPlayer, NameRegistry('localhost', port=5000), native=False)
        self.app.show(preferences)
        self.tagger = TaggerDriver(mainApplicationWindow(named('main-window'), showingOnScreen()),
                                   EventProcessingProber(timeoutInMs=ONE_SECOND),
                                   Robot())

    def stop(self):
        self.tagger.close()
        del self.tagger
        del self.app

    def new_album(self, of_type='mp3', *paths):
        self.tagger.create_album()
        self.tagger.select_audio_files(of_type, *paths)

    def shows_album_content(self, *tracks):
        self.tagger.showsAlbumContains(*tracks)

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

    def removeTrack(self, title):
        self.tagger.removeTrack(title)

    def change_track_position(self, title, to_position):
        self.tagger.moveTrack(title, to_position - 1)

    def change_settings(self, **settings):
        self.tagger.change_settings(**settings)

    def has_settings(self, **settings):
        self.tagger.hasSettings(**settings)

    def assign_isni_to_lead_performer(self):
        self.tagger.assign_isni_to_lead_performer()
        self.tagger.save_album()

    def finds_isni_of_lead_performer(self):
        self.tagger.finds_isni_of_lead_performer()
        self.tagger.save_album()