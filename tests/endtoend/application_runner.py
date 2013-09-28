# -*- coding: utf-8 -*-

import use_sip_api_v2 as sipApi
sipApi.useVersion(sipApi.VERSION_2)

from tests.cute.matchers import named, showingOnScreen
from tests.cute.widgets import mainWindow
from tests.cute.prober import EventProcessingProber
from tests.cute.robot import Robot
from tests.drivers.tagger_driver import TaggerDriver

from tgit.tagger import TGiT
from tgit.ui import main_window as main

ONE_SECOND = 1000


class ApplicationRunner(object):
    def start(self):
        self.app = TGiT('en')
        self.driver = TaggerDriver(mainWindow(named(main.MAIN_WINDOW_NAME), showingOnScreen()),
            EventProcessingProber(timeoutInMs=1000),
            Robot())

    def stop(self):
        self.driver.close()
        del self.driver
        del self.app

    def importTrack(self, path):
        self.driver.importTrack(path)

    def showsAlbumMetadata(self, **tags):
        self.driver.showsAlbumMetadata(**tags)

    def changeAlbumMetadata(self, **tags):
        self.driver.editAlbumMetadata(**tags)
        self.driver.saveTrack()

    def showsTrackMetadata(self, **tags):
        self.driver.nextStep()
        self.driver.showsTrackMetadata(**tags)

    def changeTrackMetadata(self, **tags):
        self.driver.editTrackMetadata(**tags)
        self.driver.saveTrack()