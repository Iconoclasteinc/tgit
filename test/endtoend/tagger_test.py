# -*- coding: utf-8 -*-

import shutil
import unittest

from tgit.util import fs
from test.drivers.application_settings_driver import ApplicationSettingsDriver
from test.util import resources, doubles
from test.endtoend.application_runner import ApplicationRunner


class TaggerTest(unittest.TestCase):
    def setUp(self):
        self.tempDir = resources.makeTempDir()
        self.library = doubles.recordingLibrary(self.tempDir)
        self.settings = ApplicationSettingsDriver()
        self.settings.set('language', 'en')
        self.application = ApplicationRunner()
        self.application.start(self.settings.preferences)

    def tearDown(self):
        self.application.stop()
        self.settings.destroy()
        self.library.delete()
        shutil.rmtree(self.tempDir)

    def restart(self):
        self.application.stop()
        self.application = ApplicationRunner()
        self.application.start(self.settings.preferences)

    def testCreatesAndTagsANewAlbum(self):
        tracks = [
            self.library.create(trackTitle='Ma préférence',
                                releaseName='Jaloux',
                                frontCover=('image/jpeg', 'Cover', fs.readContent(resources.path('jaloux.jpg'))),
                                leadPerformer='Julien Clerc',
                                labelName='EMI',
                                releaseTime='1978'),
            self.library.create(trackTitle='Fais moi une place',
                                releaseName='Fais moi une place',
                                frontCover=('image/jpeg', 'Cover', fs.readContent(resources.path('une-place.jpg'))),
                                labelName='Virgin',
                                releaseTime='1990',
                                upc='3268440307258'),
            self.library.create(trackTitle="Ce n'est rien",
                                releaseName='Niagara',
                                frontCover=('image/jpeg', 'Cover', fs.readContent(resources.path('niagara.jpg'))),
                                releaseTime='1971',
                                lyricist='Étienne Roda-Gil')
        ]

        self.application.newAlbum(*tracks)
        self.application.showsAlbumContent(['Ma préférence'],
                                           ['Fais moi une place'],
                                           ["Ce n'est rien"])

        self.application.showsAlbumMetadata(releaseName='Jaloux', leadPerformer='Julien Clerc', labelName='EMI',
                                            releaseTime='1978')
        self.application.changeAlbumMetadata(releaseName='Best Of', frontCover=resources.path('best-of.jpg'),
                                             labelName='EMI Music France', releaseTime='2009-04-06')

        self.application.showsNextTrackMetadata(trackTitle='Ma préférence')
        self.application.changeTrackMetadata(composer='Julien Clerc', lyricist='Jean-Loup Dabadie')

        self.application.showsNextTrackMetadata(trackTitle='Fais moi une place')
        self.application.changeTrackMetadata(composer='Julien Clerc', lyricist='Francoise Hardy')

        self.application.showsNextTrackMetadata(trackTitle="Ce n'est rien")
        self.application.changeTrackMetadata(composer='Julien Clerc')

        self.library.contains('Julien Clerc - 01 - Ma préférence.mp3',
                              frontCover=(resources.path('best-of.jpg'), 'Front Cover'),
                              releaseName='Best Of',
                              leadPerformer='Julien Clerc',
                              labelName='EMI Music France',
                              releaseTime='2009-04-06',
                              trackTitle='Ma préférence',
                              composer='Julien Clerc',
                              lyricist='Jean-Loup Dabadie')
        self.library.contains('Julien Clerc - 02 - Fais moi une place.mp3',
                              frontCover=(resources.path('best-of.jpg'), 'Front Cover'),
                              releaseName='Best Of',
                              leadPerformer='Julien Clerc',
                              labelName='EMI Music France',
                              releaseTime='2009-04-06',
                              trackTitle='Fais moi une place',
                              composer='Julien Clerc',
                              lyricist='Francoise Hardy')
        self.library.contains("Julien Clerc - 03 - Ce n'est rien.mp3",
                              frontCover=(resources.path('best-of.jpg'), 'Front Cover'),
                              releaseName='Best Of',
                              leadPerformer='Julien Clerc',
                              labelName='EMI Music France',
                              releaseTime='2009-04-06',
                              trackTitle="Ce n'est rien",
                              composer='Julien Clerc',
                              lyricist='Étienne Roda-Gil')

    def testChangingApplicationSettings(self):
        self.application.hasSettings(language='English')
        self.application.changeSettings(language='French')
        self.settings.hasStored('language', 'fr')
        self.restart()
        self.application.hasSettings(language='Français')