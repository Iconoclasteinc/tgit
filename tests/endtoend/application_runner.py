# -*- coding: utf-8 -*-

from tgit.tagger import TGiT

from tests.util import project
from tests.cute.events import MainEventLoop
from .tgit_driver import TGiTDriver

ONE_SECOND = 1000


class ApplicationRunner(object):
    def start(self):
        self._app = TGiT(project.locales_dir)
        self._tgit = TGiTDriver(timeout_in_ms=ONE_SECOND)
        self._wait_for_window_shown()

    def _wait_for_window_shown(self):
        MainEventLoop.process_pending_events()

    def stop(self):
        self._tgit.close()
        del self._tgit
        del self._app

    def select_music_file(self, path):
        self._tgit.add_file(path)

    def shows_music_metadata(self, artist, album, title, bitrate, duration):
        self._tgit.shows_album_metadata(album_title=album, bitrate=bitrate, duration=duration)
