# -*- coding: utf-8 -*-

import use_sip_api_v2 as sipApi

sipApi.useVersion(sipApi.VERSION_2)

from tgit.tagger import TGiT
from tgit import audio
from tgit.ui import main_window as main

from tests.cute.matchers import named, showingOnScreen
from tests.cute.widgets import mainWindow
from tests.cute.prober import EventProcessingProber
from tests.cute.robot import Robot
from tests.drivers.tagger_driver import TaggerDriver

ONE_SECOND = 1000


class ApplicationRunner(object):
    def start(self):
        self.app = TGiT('en', audio.noSound())
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