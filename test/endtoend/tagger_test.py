# -*- coding: utf-8 -*-

import unittest

from test.util import resources
from test.util.mp3 import makeMp3
from test.util.fakes import FakeAudioLibrary
from test.endtoend.application_runner import ApplicationRunner

from tgit import fs


class TaggerTest(unittest.TestCase):
    def setUp(self):
        self.application = ApplicationRunner()
        self.audioLibrary = FakeAudioLibrary()
        self.application.start()

    def tearDown(self):
        self.application.stop()
        self.audioLibrary.delete()

    def testTaggingASingleTrackWithAlbumAndTrackMetadata(self):
        track = self.audioLibrary.add(makeMp3())

        self.application.newAlbum(track.filename)
        self.application.showsAlbumContent([u''])

        self.application.showsAlbumMetadata(
            releaseName=u'',
            leadPerformer=u'',
            labelName=u'',
            catalogNumber=u'',
            upc=u'',
            recordingTime=u'',
            releaseTime='')
        self.application.changeAlbumMetadata(
            frontCover=resources.path('sheller-en-solitaire.jpg'),
            releaseName=u'Sheller en solitaire',
            leadPerformer=u'William Sheller',
            labelName=u'Philips',
            catalogNumber=u'848 786-2',
            upc=u'042284878623',
            recordingTime=u'1991',
            releaseTime=u'1991')

        self.application.showsNextTrackMetadata(
            trackTitle=u'',
            bitrate='320 kbps',
            duration='00:09',
            isrc=u'')
        self.application.changeTrackMetadata(
            trackTitle=u'Un homme heureux',
            versionInfo=u'Version originale',
            isrc=u'FRZ039105290')
        self.audioLibrary.containsFile(
            track.filename,
            frontCover=resources.path('sheller-en-solitaire.jpg'),
            releaseName=u'Sheller en solitaire',
            leadPerformer=u'William Sheller',
            labelName=u'Philips',
            catalogNumber=u'848 786-2',
            upc=u'042284878623',
            recordingTime=u'1991',
            releaseTime=u'1991',
            trackTitle=u'Un homme heureux',
            versionInfo=u'Version originale',
            isrc=u'FRZ039105290')


    def testTaggingMultipleTracksInAnAlbum(self):
        maPreference = self.audioLibrary.add(makeMp3(
            trackTitle=u'Ma préférence',
            leadPerformer='Julien Clerc',
            frontCover=('image/gif', 'Front Cover',
                        fs.readContent(resources.path('triple-best-of.gif')))))
        faisMoiUnePlace = self.audioLibrary.add(makeMp3(trackTitle=u'Fais moi une place'))
        ceNestRien = self.audioLibrary.add(makeMp3(trackTitle=u"Ce n'est rien"))

        self.application.newAlbum(maPreference.filename)
        self.application.importTrack(faisMoiUnePlace.filename)
        self.application.importTrack(ceNestRien.filename)
        self.application.showsAlbumContent([u'Ma préférence', '', ''],
                                           [u'Fais moi une place', '', ''],
                                           [u"Ce n'est rien"])
        self.application.showsAlbumMetadata(leadPerformer='Julien Clerc')
        self.application.changeAlbumMetadata(
            releaseName='Triple Best Of',
            labelName='EMI France')
        self.application.showsNextTrackMetadata(trackTitle=u'Ma préférence')
        self.application.changeTrackMetadata(versionInfo='Compilation')
        self.application.showsNextTrackMetadata(trackTitle=u'Fais moi une place')
        self.application.changeTrackMetadata(versionInfo='Compilation')
        self.application.showsNextTrackMetadata(trackTitle=u"Ce n'est rien")
        self.application.changeTrackMetadata(versionInfo='Compilation')

        self.audioLibrary.containsFile(maPreference.filename,
                                       frontCover=resources.path('triple-best-of.gif'),
                                       releaseName='Triple Best Of',
                                       leadPerformer='Julien Clerc',
                                       labelName='EMI France',
                                       trackTitle=u'Ma préférence',
                                       versionInfo='Compilation')
        self.audioLibrary.containsFile(faisMoiUnePlace.filename,
                                       frontCover=resources.path('triple-best-of.gif'),
                                       releaseName='Triple Best Of',
                                       leadPerformer='Julien Clerc',
                                       labelName='EMI France',
                                       trackTitle=u'Fais moi une place',
                                       versionInfo='Compilation')
        self.audioLibrary.containsFile(ceNestRien.filename,
                                       frontCover=resources.path('triple-best-of.gif'),
                                       releaseName='Triple Best Of',
                                       leadPerformer='Julien Clerc',
                                       labelName='EMI France',
                                       trackTitle=u"Ce n'est rien",
                                       versionInfo='Compilation')

    def testChangingTheAlbumCompositionFromTheTrackList(self):
        myNameIsJonasz = self.audioLibrary.add(makeMp3(trackTitle='My name is JONASZ'))
        ditesMoi = self.audioLibrary.add(makeMp3(trackTitle='Dites-moi'))
        fanfan = self.audioLibrary.add(makeMp3(trackTitle='Fanfan', releaseName='?'))
        superNana = self.audioLibrary.add(makeMp3(trackTitle='Supernana'))

        self.application.newAlbum(myNameIsJonasz.filename)
        self.application.importTrack(ditesMoi.filename)
        self.application.importTrack(fanfan.filename)
        self.application.importTrack(superNana.filename)

        self.application.showsAlbumContent(['My name is JONASZ'],
                                           ['Dites-moi'],
                                           ['Fanfan'],
                                           ['Supernana'])
        self.application.changeTrackPosition('My name is JONASZ', 4)
        self.application.changeTrackPosition('Supernana', 2)
        self.application.removeTrack('Fanfan')
        self.application.showsAlbumContent(['Dites-moi'],
                                           ['Supernana'],
                                           ['My name is JONASZ'])

        self.application.showsAlbumMetadata()
        self.application.changeAlbumMetadata(releaseName='Michel Jonasz')
        self.application.showsNextTrackMetadata(trackTitle='Dites-moi')
        self.application.showsNextTrackMetadata(trackTitle='Supernana')
        self.application.showsNextTrackMetadata(trackTitle='My name is JONASZ')

        self.audioLibrary.containsFile(ditesMoi.filename, releaseName='Michel Jonasz')
        self.audioLibrary.containsFile(superNana.filename, releaseName='Michel Jonasz')
        self.audioLibrary.containsFile(myNameIsJonasz.filename, releaseName='Michel Jonasz')
        self.audioLibrary.containsFile(fanfan.filename, releaseName='?')
