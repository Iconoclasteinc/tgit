# -*- coding: utf-8 -*-

import sip

from test.cute.matchers import named, showingOnScreen
from test.cute.widgets import mainApplicationWindow
from test.cute.prober import EventProcessingProber
from test.cute.robot import Robot
from test.drivers.tagger_driver import TaggerDriver
from test.util import fakes

from tgit.tagger import TGiT
from tgit.ui import constants as ui
from tgit.ui.dialogs import AudioFileChooserDialog, ImageFileChooserDialog

ENGLISH = 'en'
ONE_SECOND = 1000


class ApplicationRunner(object):
    def start(self):
        self.app = TGiT(ENGLISH, fakes.audioPlayer, AudioFileChooserDialog(native=False),
                        ImageFileChooserDialog(native=False))
        self.app.show()
        self.tagger = TaggerDriver(mainApplicationWindow(named(ui.MAIN_WINDOW_NAME),
                                                         showingOnScreen()),
                                   EventProcessingProber(timeoutInMs=ONE_SECOND),
                                   Robot())

    def stop(self):
        self.tagger.close()
        del self.tagger
        # force deletion of C++ objects in the background, for extra safety
        sip.delete(self.app)
        del self.app

    def newAlbum(self, path):
        self.tagger.createAlbum()
        self.tagger.selectAudioFile(path)

    def addTrack(self, path):
        self.tagger.addTrack(path)

    def showsAlbumContent(self, *tracks):
        self.tagger.showsAlbumContains(*tracks)

    def showsAlbumMetadata(self, **tags):
        self.tagger.toAlbum()
        self.tagger.showsAlbumMetadata(**tags)
        # todo navigate back to track list
        # so we always no where we're starting from

    def changeAlbumMetadata(self, **tags):
        self.tagger.editAlbumMetadata(**tags)
        self.tagger.saveAlbum()

    def showsNextTrackMetadata(self, **tags):
        self.tagger.toNextTrack()
        self.tagger.showsTrackMetadata(**tags)

    def changeTrackMetadata(self, **tags):
        self.tagger.editTrackMetadata(**tags)
        self.tagger.saveAlbum()

    def removeTrack(self, title):
        self.tagger.removeTrack(title)

    def changeTrackPosition(self, title, to):
        self.tagger.moveTrack(title, to - 1)