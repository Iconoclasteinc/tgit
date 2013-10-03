# -*- coding: utf-8 -*-

import use_sip_api_v2 as sipApi
sipApi.useVersion(sipApi.VERSION_2)

from tgit.tagger import TGiT
from tgit.audio_player import NullAudio
from tgit.ui import main_window as main

from tests.cute.matchers import named, showingOnScreen
from tests.cute.widgets import mainWindow
from tests.cute.prober import EventProcessingProber
from tests.cute.robot import Robot
from tests.drivers.tagger_driver import TaggerDriver

ONE_SECOND = 1000


class ApplicationRunner(object):
    def start(self):
        self.app = TGiT('en', NullAudio())
        self.driver = TaggerDriver(mainWindow(named(main.MAIN_WINDOW_NAME), showingOnScreen()),
            EventProcessingProber(timeoutInMs=1000),
            Robot())

    def stop(self):
        self.driver.close()
        del self.driver
        del self.app

    def importTrack(self, path):
        self.driver.importTrack(path)

    def showsAlbumContent(self, *tracks):
        self.driver.showsAlbumContains(*tracks)

    def showsAlbumMetadata(self, **tags):
        self.driver.showsAlbumMetadata(**tags)

    def changeAlbumMetadata(self, **tags):
        self.driver.editAlbumMetadata(**tags)
        self.driver.saveTrack()

    def showsTrackMetadata(self, **tags):
        self.driver.showsTrackMetadata(**tags)

    def changeTrackMetadata(self, **tags):
        self.driver.editTrackMetadata(**tags)
        self.driver.saveTrack()