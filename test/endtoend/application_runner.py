# -*- coding: utf-8 -*-

import sip
from test.cute.events import MainEventLoop
from tgit.sources.isni import NameRegistry
from tgit.util import sip_api
sip_api.use_v2()

from test.cute.matchers import named, showingOnScreen
from test.cute.widgets import mainApplicationWindow
from test.cute.prober import EventProcessingProber
from test.cute.robot import Robot
from test.drivers.tagger_driver import TaggerDriver
from test.util import doubles
from tgit.tagger import TGiT

ONE_SECOND = 1000


class ApplicationRunner(object):
    def start(self, preferences):
        self.app = TGiT(doubles.audioPlayer, NameRegistry('localhost', 5000), native=False)
        self.app.show(preferences)
        self.tagger = TaggerDriver(mainApplicationWindow(named('main-window'), showingOnScreen()),
                                   EventProcessingProber(timeoutInMs=ONE_SECOND),
                                   Robot())

    def stop(self):
        self.tagger.close()
        del self.tagger
        # force deletion of C++ objects in the background, for extra safety
        sip.delete(self.app)
        del self.app

    def newAlbum(self, *paths):
        self.tagger.createAlbum()
        self.tagger.selectAudioFiles(*paths)

    def showsAlbumContent(self, *tracks):
        self.tagger.showsAlbumContains(*tracks)

    def showsAlbumMetadata(self, **tags):
        self.tagger.next()
        self.tagger.showsAlbumMetadata(**tags)
        MainEventLoop.processEventsFor(500)
        # todo navigate back to track list
        # so we always no where we're starting from

    def changeAlbumMetadata(self, **tags):
        self.tagger.editAlbumMetadata(**tags)
        self.tagger.saveAlbum()

    def showsNextTrackMetadata(self, **tags):
        self.tagger.next()
        self.tagger.showsTrackMetadata(**tags)

    def changeTrackMetadata(self, **tags):
        self.tagger.editTrackMetadata(**tags)
        self.tagger.saveAlbum()

    def removeTrack(self, title):
        self.tagger.removeTrack(title)

    def changeTrackPosition(self, title, to):
        self.tagger.moveTrack(title, to - 1)

    def changeSettings(self, **settings):
        self.tagger.changeSettings(**settings)

    def hasSettings(self, **settings):
        self.tagger.hasSettings(**settings)