# -*- coding: utf-8 -*-

from PyQt4.QtCore import Qt, QDir
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


class TrackSelectionDialog(TrackSelector):
    def __init__(self, parent=None, native=False):
        TrackSelector.__init__(self)
        self._parent = parent
        self._native = native
        self._dialog = None

    def _makeDialog(self, parent):
        dialog = QFileDialog(parent)
        dialog.setObjectName(SELECT_TRACK_DIALOG_NAME)
        dialog.setDirectory(QDir.homePath())
        dialog.setNameFilter('%s (*.mp3)' % dialog.tr('Audio files'))
        dialog.setOption(QFileDialog.DontUseNativeDialog, not self._native)
        dialog.fileSelected.connect(self._signalTrackSelected)
        return dialog

    def useNativeLookAndFeel(self, native):
        self._native = native

    def selectTrack(self):
        if not self._dialog:
            self._dialog = self._makeDialog(self._parent)
        self._dialog.open()