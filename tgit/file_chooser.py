# -*- coding: utf-8 -*-

from tgit.announcer import Announcer


class FileChoiceListener(object):
    def fileChosen(self, filename):
        pass


class FileChooser(object):
    def __init__(self):
        super(FileChooser, self).__init__()
        self._listeners = Announcer()

    def chooseFile(self):
        pass

    def addChoiceListener(self, listener):
        self._listeners.addListener(listener)

    def _signalFileChosen(self, filename):
        self._listeners.fileChosen(filename)
