# -*- coding: utf-8 -*-

from tgit.tagger import TGiT

from tests.util import project
from tests.cute.events import MainEventLoop
from .tgit_driver import TGiTDriver

ONE_SECOND = 1000


class ApplicationRunner(object):
    def start(self):
        self._app = TGiT(project.locales_dir)
        self._driver = TGiTDriver(timeout_in_ms=ONE_SECOND)
        self._wait_for_window_shown()

    def _wait_for_window_shown(self):
        MainEventLoop.process_pending_events()

    def stop(self):
        self._driver.close()
        del self._driver
        del self._app

    def import_audio_file(self, path):
        self._driver.add_file(path)

    def shows_metadata(self, **tags):
        self._driver.shows_metadata(tags)

    def change_metadata(self, **tags):
        self._driver.edit_metadata(tags)
        self._driver.save_audio_file()
