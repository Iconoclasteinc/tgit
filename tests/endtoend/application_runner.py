# -*- coding: utf-8 -*-

import use_sip_api_v2
from tgit.tagger import TGiT

from tests.endtoend.tgit_driver import TGiTDriver

ONE_SECOND = 1000


class ApplicationRunner(object):
    def start(self):
        self.app = TGiT('en')
        self.driver = TGiTDriver(timeoutInMs=ONE_SECOND)

    def stop(self):
        self.driver.close()
        del self.driver
        del self.app

    def importTrack(self, path):
        self.driver.importTrack(path)

    def showsMetadata(self, **tags):
        self.driver.showsMetadata(**tags)

    def changeMetadata(self, **tags):
        self.driver.editMetadata(**tags)
        self.driver.saveTrack()