# -*- coding: utf-8 -*-

import use_sip_api_v2 as sipApi
sipApi.useVersion(sipApi.VERSION_2)
from tgit.tagger import TGiT

from tests.drivers.tagger_driver import TaggerDriver

ONE_SECOND = 1000


class ApplicationRunner(object):
    def start(self):
        self.app = TGiT('en')
        self.driver = TaggerDriver(timeoutInMs=ONE_SECOND)

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