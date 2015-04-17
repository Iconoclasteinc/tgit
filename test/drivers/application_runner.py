# -*- coding: utf-8 -*-
from test.cute.events import MainEventLoop
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
        self.app = TGiT(doubles.audioPlayer, NameRegistry('localhost', 5000), native=False)
        self.app.show(preferences)
        self.tagger = TaggerDriver(mainApplicationWindow(named('main-window'), showingOnScreen()),
                                   EventProcessingProber(timeoutInMs=ONE_SECOND),
                                   Robot())

    def stop(self):
        self.tagger.close()
        del self.tagger
        del self.app

    def newAlbum(self, *paths):
        self.tagger.createAlbum()
        self.tagger.selectAudioFiles(*paths)

    def shows_album_content(self, *tracks):
        self.tagger.showsAlbumContains(*tracks)

    def shows_album_metadata(self, **tags):
        self.tagger.next()
        self.tagger.showsAlbumMetadata(**tags)
        MainEventLoop.processEventsFor(500)
        # todo navigate back to track list
        # so we always no where we're starting from

    def change_album_metadata(self, **tags):
        self.tagger.editAlbumMetadata(**tags)
        self.tagger.saveAlbum()

    def shows_next_track_metadata(self, **tags):
        self.tagger.next()
        self.tagger.showsTrackMetadata(**tags)

    def change_track_metadata(self, **tags):
        self.tagger.editTrackMetadata(**tags)
        self.tagger.saveAlbum()

    def removeTrack(self, title):
        self.tagger.removeTrack(title)

    def changeTrackPosition(self, title, to):
        self.tagger.moveTrack(title, to - 1)

    def change_settings(self, **settings):
        self.tagger.change_settings(**settings)

    def has_settings(self, **settings):
        self.tagger.hasSettings(**settings)