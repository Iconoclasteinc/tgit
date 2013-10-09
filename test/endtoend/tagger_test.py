# -*- coding: utf-8 -*-

import unittest

from test.util import resources
from test.util.mp3_maker import MP3
from test.endtoend.application_runner import ApplicationRunner
from test.util.fake_audio_library import FakeAudioLibrary

SAMPLE_AUDIO_FILE = resources.path("Hallelujah.mp3")


def copy(track):
    return MP3(track)


def mp3(**tags):
    return MP3(**tags)


class TaggerTest(unittest.TestCase):
    def setUp(self):
        self.application = ApplicationRunner()
        self.audioLibrary = FakeAudioLibrary()
        self.application.start()

    def tearDown(self):
        self.application.stop()
        self.audioLibrary.delete()

    # todo create a test mp3 from a sample realistic mpeg frame and make expected values explicit
    def testTaggingASingleTrackAndSavingChanges(self):
        track = self.audioLibrary.add(copy(SAMPLE_AUDIO_FILE))

        self.application.importTrack(track.filename)
        self.application.showsAlbumContent('Hallelujah (Chorus)')
        self.application.showsAlbumMetadata(
            releaseName='Messiah',
            leadPerformer='The Sixteen - Harry Christophers')
        self.application.changeAlbumMetadata(
            frontCoverPicture=resources.path("minions-in-black.jpg"),
            releaseName='Despicable Me',
            leadPerformer='Tim, Mark and Phil')
        self.application.showsTrackMetadata(
            trackTitle='Hallelujah (Chorus)',
            duration='03:56')
        self.application.changeTrackMetadata(
            trackTitle='Potato Banana Song',
            featuredGuest='Stuart')
        self.audioLibrary.containsFile(
            track.filename,
            releaseName='Despicable Me',
            leadPerformer='Tim, Mark and Phil',
            trackTitle='Potato Banana Song',
            featuredGuest='Stuart',
            frontCoverFile=resources.path("minions-in-black.jpg"))

    def testTaggingMultipleTracksFromTheSameAlbum(self):
        track1 = self.audioLibrary.add(mp3(releaseName='Album Title', trackTitle='Track 1'))
        track2 = self.audioLibrary.add(mp3(releaseName='Album Title', trackTitle='Track 2'))

        self.application.importTrack(track1.filename)
        self.application.importTrack(track2.filename)
        self.application.showsAlbumContent('Track 1', 'Track 2')
        self.application.showsAlbumMetadata(releaseName='Album Title')
        self.application.changeAlbumMetadata(releaseName='Despicable Me')
        self.application.showsTrackMetadata(trackTitle='Track 1')
        self.application.changeTrackMetadata(trackTitle='Potato Banana Song')
        self.application.showsTrackMetadata(trackTitle='Track 2')
        self.application.changeTrackMetadata(trackTitle='Potato Banana Song (Remix)')

        self.audioLibrary.containsFile(track1.filename,
                                       releaseName='Despicable Me',
                                       trackTitle='Potato Banana Song')
        self.audioLibrary.containsFile(track2.filename,
                                       releaseName='Despicable Me',
                                       trackTitle='Potato Banana Song (Remix)')

    # todo Consider exercising the different ways of adding a track
    def managingTheAlbumFromTheTrackList(self):
        track1 = self.audioLibrary.add(mp3(releaseName='Album Title', trackTitle='Track 1'))
        track2 = self.audioLibrary.add(mp3(releaseName='Album Title', trackTitle='Track 2'))
        track3 = self.audioLibrary.add(mp3(releaseName='Album Title', trackTitle='Track 3'))

        self.application.importTrack(track1.filename)
        self.application.importTrack(track2.filename)
        self.application.importTrack(track3.filename)

        self.application.showsAlbumContent('Track 1', 'Track 2', 'Track 3')
        self.application.removeTrack('Track 1')
        self.application.removeTrack('Track 2')
        self.application.showsAlbumMetadata(releaseName='Album Title')
        self.application.changeAlbumMetadata(releaseName='New Album Title')
        self.application.showsTrackMetadata(trackTitle='Track 3')

        self.audioLibrary.containsFile(track1.filename, releaseName='Album Title')
        self.audioLibrary.containsFile(track2.filename, releaseName='Album Title')
        self.audioLibrary.containsFile(track3.filename, releaseName='New Album Title')
