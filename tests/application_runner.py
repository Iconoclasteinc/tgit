# -*- coding: utf-8 -*-

from tgit.tgit import TGiT

from tgit_driver import TGiTDriver

ONE_SECOND = 1000


class ApplicationRunner(object):
    def start(self):
        self.app = TGiT()
        self.tgit = TGiTDriver(timeout_in_ms=ONE_SECOND)

    def stop(self):
        self.tgit.close()
        del self.app

    def say_hello(self):
        self.tgit.display_message()