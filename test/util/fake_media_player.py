# -*- coding: utf-8 -*-


class FakeMediaPlayer(object):
    def __init__(self):
        self.track = None

    def isPlaying(self):
        return self.track is not None

    def play(self, track):
        self.track = track

    def stop(self):
        self.track = None

    def addMediaListener(self, listener):
        pass
