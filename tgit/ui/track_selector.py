# -*- coding: utf-8 -*-

from PyQt4.QtCore import QDir
from PyQt4.QtGui import QFileDialog

from tgit.announcer import Announcer


SELECT_TRACK_DIALOG_NAME = "Select Track File"


class TrackSelectionListener(object):
    def trackSelected(self, filename):
        pass


class TrackSelector(object):
    def __init__(self):
        super(TrackSelector, self).__init__()
        self._listeners = Announcer()

    def selectTrack(self):
        pass

    def addSelectionListener(self, listener):
        self._listeners.add(listener)

    def _signalTrackSelected(self, filename):
        self._listeners.announce().trackSelected(filename)


class TrackSelectionDialog(QFileDialog, TrackSelector):
    def __init__(self, parent=None):
        QFileDialog.__init__(self, parent)
        TrackSelector.__init__(self)

        self.setObjectName(SELECT_TRACK_DIALOG_NAME)
        self.setDirectory(QDir.homePath())
        self.setOption(QFileDialog.DontUseNativeDialog)
        self.setNameFilter(self.tr("MP3 files") + " (*.mp3)")
        self.setModal(True)
        self.fileSelected.connect(self._signalTrackSelected)

    def selectTrack(self):
        self.open()