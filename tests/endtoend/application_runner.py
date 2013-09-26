# -*- coding: utf-8 -*-

import use_sip_api_v2
from tgit.tagger import TGiT

from tests.endtoend.tgit_driver import TGiTDriver

ONE_SECOND = 1000


class ApplicationRunner(object):
    def start(self):
        self._app = TGiT('en')
        self._driver = TGiTDriver(timeout_in_ms=ONE_SECOND)

    def stop(self):
        self._driver.close()
        del self._driver
        del self._app

    def importTrack(self, path):
        self._driver.importTrack(path)

    def showsMetadata(self, **tags):
        self._driver.showsMetadata(tags)

    def changeMetadata(self, **tags):
        self._driver.editMetadata(tags)
        self._driver.saveTrack()
