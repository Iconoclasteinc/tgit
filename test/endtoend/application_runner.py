# -*- coding: utf-8 -*-

import sip
# noinspection PyUnresolvedReferences
import use_sip_api_v2

from tgit.tagger import TGiT
from tgit.null import Null
from tgit.ui import main_window as main

from test.cute.matchers import named, showingOnScreen
from test.cute.widgets import mainWindow
from test.cute.prober import EventProcessingProber
from test.cute.robot import Robot
from test.drivers.tagger_driver import TaggerDriver

ONE_SECOND = 1000


class ApplicationRunner(object):
    def start(self):
        self.app = TGiT(locale='en', player=Null())
        self.tagger = TaggerDriver(mainWindow(named(main.MAIN_WINDOW_NAME), showingOnScreen()),
                                   EventProcessingProber(timeoutInMs=ONE_SECOND),
                                   Robot())

    def stop(self):
        self.tagger.close()
        del self.tagger
        sip.delete(self.app)
        del self.app

    def importTrack(self, path):
        self.tagger.importTrack(path)

    def showsAlbumContent(self, *tracks):
        self.tagger.showsAlbumContains(*tracks)

    def showsAlbumMetadata(self, **tags):
        self.tagger.navigateToAlbumMetadata()
        self.tagger.showsAlbumMetadata(**tags)
        # todo navigate back to track list
        # so we always no where we're starting from

    # todo pass the track index as parameter
    def changeAlbumMetadata(self, **tags):
        self.tagger.editAlbumMetadata(**tags)
        self.tagger.saveAlbum()

    # todo pass the track index as parameter
    def showsTrackMetadata(self, **tags):
        self.tagger.navigateToTrackMetadata()
        self.tagger.showsTrackMetadata(**tags)

    # todo pass the track index as parameter
    def changeTrackMetadata(self, **tags):
        self.tagger.editTrackMetadata(**tags)
        self.tagger.saveAlbum()

    def removeTrack(self, title):
        self.tagger.removeTrack(title)