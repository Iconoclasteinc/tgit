# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences
import use_sip_api_v2

from tgit.tagger import TGiT
from tgit.null import Null
from tgit.ui import main_window as main

from test.cute.matchers import named, showingOnScreen
from test.cute.widgets import mainWindow
from test.cute.prober import EventProcessingProber
from test.cute.robot import Robot
from test.drivers.tagger_driver import TaggerDriver

ONE_SECOND = 1000


class ApplicationRunner(object):
    def start(self):
        self.app = TGiT(locale='en', player=Null())
        self.tagger = TaggerDriver(mainWindow(named(main.MAIN_WINDOW_NAME), showingOnScreen()),
                                   EventProcessingProber(timeoutInMs=ONE_SECOND),
                                   Robot())

    def stop(self):
        self.tagger.close()
        del self.tagger
        del self.app

    def importTrack(self, path):
        self.tagger.importTrack(path)

    def showsAlbumContent(self, *tracks):
        self.tagger.showsAlbumContains(*tracks)

    def showsAlbumMetadata(self, **tags):
        self.tagger.navigateToAlbumMetadata()
        self.tagger.showsAlbumMetadata(**tags)

    def changeAlbumMetadata(self, **tags):
        self.tagger.editAlbumMetadata(**tags)
        self.tagger.saveAlbum()

    def showsTrackMetadata(self, **tags):
        self.tagger.navigateToTrackMetadata()
        self.tagger.showsTrackMetadata(**tags)

    def changeTrackMetadata(self, **tags):
        self.tagger.editTrackMetadata(**tags)
        self.tagger.saveAlbum()