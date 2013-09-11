# -*- coding: utf-8 -*-

import os

from tgit.tgit import TGiT

from tgit_driver import TGiTDriver

ONE_SECOND = 1000

locales_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'locales'))


class ApplicationRunner(object):
    def start(self):
        self._app = TGiT(locales_dir)
        self._tgit = TGiTDriver(timeout_in_ms=ONE_SECOND)

    def stop(self):
        self._tgit.close()
        del self._tgit
        del self._app

    def select_music_file(self, filename):
        self._tgit.open_file(filename)

    def shows_music_metadata(self, artist, album, title, bitrate, duration):
        self._tgit.shows_music_title(title)