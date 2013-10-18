# -*- coding: utf-8 -*-


class FakeMediaPlayer(object):
    def __init__(self):
        self.track = None

    def currentTrack(self):
        return self.track

    def isPlaying(self):
        return self.currentTrack() is not None

    def play(self, track):
        self.track = track

    def stop(self):
        self.track = None

    def addMediaListener(self, listener):
        pass
