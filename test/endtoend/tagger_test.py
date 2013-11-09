# -*- coding: utf-8 -*-

import unittest

from test.util import resources
from test.util.mp3_file import makeMp3
from test.util.fakes import FakeMetadataStore
from test.endtoend.application_runner import ApplicationRunner

from tgit.util import fs


class TaggerTest(unittest.TestCase):
    def setUp(self):
        self.application = ApplicationRunner()
        self.audioLibrary = FakeMetadataStore()
        self.application.start()

    def tearDown(self):
        self.application.stop()
        self.audioLibrary.delete()

    def testCreatesAndTagsANewAlbum(self):
        maPreference = self.audioLibrary.add(makeMp3(
            trackTitle=u'Ma préférence',
            releaseName='Jaloux',
            frontCover=('image/jpeg', 'Cover', fs.readContent(resources.path('jaloux.jpg'))),
            leadPerformer='Julien Clerc',
            labelName='EMI',
            releaseTime='1978'))
        faisMoiUnePlace = self.audioLibrary.add(makeMp3(
            trackTitle='Fais moi une place',
            releaseName='Fais moi une place',
            frontCover=('image/jpeg', 'Cover', fs.readContent(resources.path('une-place.jpg'))),
            labelName='Virgin',
            releaseTime='1990',
            upc='3268440307258'))
        rolo = self.audioLibrary.add(makeMp3(
            trackTitle='Rolo le Baroudeur',
            releaseName='Niagara',
            frontCover=('image/jpeg', 'Cover', fs.readContent(resources.path('niagara.jpg'))),
            releaseTime='1971',
            lyricist=u'Étienne Roda-Gil'
        ))
        ceNestRien = self.audioLibrary.add(makeMp3(
            trackTitle="Ce n'est rien",
            releaseName='Niagara',
            frontCover=('image/jpeg', 'Cover', fs.readContent(resources.path('niagara.jpg'))),
            releaseTime='1971',
            lyricist=u'Étienne Roda-Gil'))

        self.application.newAlbum(maPreference)
        self.application.importTrack(faisMoiUnePlace)
        self.application.importTrack(rolo)
        self.application.importTrack(ceNestRien)

        self.application.showsAlbumContent([u'Ma préférence'],
                                           [u'Fais moi une place'],
                                           [u'Rolo le Baroudeur'],
                                           [u"Ce n'est rien"])
        self.application.removeTrack('Rolo le Baroudeur')
        self.application.changeTrackPosition(u"Ce n'est rien", 1)

        self.application.showsAlbumMetadata(
            releaseName='Jaloux',
            leadPerformer='Julien Clerc',
            labelName='EMI',
            releaseTime='1978')
        self.application.changeAlbumMetadata(
            releaseName='Best Of',
            frontCover=resources.path('best-of.jpg'),
            labelName='EMI Music France',
            releaseTime='2009-04-06')

        self.application.showsNextTrackMetadata(trackTitle=u"Ce n'est rien")
        self.application.changeTrackMetadata(
            composer='Julien Clerc')

        self.application.showsNextTrackMetadata(trackTitle=u'Ma préférence')
        self.application.changeTrackMetadata(
            composer='Julien Clerc',
            lyricist='Jean-Loup Dabadie')

        self.application.showsNextTrackMetadata(trackTitle=u'Fais moi une place')
        self.application.changeTrackMetadata(
            composer='Julien Clerc',
            lyricist='Francoise Hardy')

        self.audioLibrary.contains(maPreference,
                                   frontCover=(resources.path('best-of.jpg'), 'Front Cover'),
                                   releaseName='Best Of',
                                   leadPerformer='Julien Clerc',
                                   labelName='EMI Music France',
                                   releaseTime='2009-04-06',
                                   trackTitle=u'Ma préférence',
                                   composer='Julien Clerc',
                                   lyricist='Jean-Loup Dabadie')
        self.audioLibrary.contains(faisMoiUnePlace,
                                   frontCover=(resources.path('best-of.jpg'), 'Front Cover'),
                                   releaseName='Best Of',
                                   leadPerformer='Julien Clerc',
                                   labelName='EMI Music France',
                                   releaseTime='2009-04-06',
                                   trackTitle=u'Fais moi une place',
                                   composer='Julien Clerc',
                                   lyricist='Francoise Hardy')
        self.audioLibrary.contains(ceNestRien,
                                   frontCover=(resources.path('best-of.jpg'), 'Front Cover'),
                                   releaseName='Best Of',
                                   leadPerformer='Julien Clerc',
                                   labelName='EMI Music France',
                                   releaseTime='2009-04-06',
                                   trackTitle=u"Ce n'est rien",
                                   composer='Julien Clerc',
                                   lyricist=u'Étienne Roda-Gil')
        self.audioLibrary.contains(rolo,
                                   releaseName='Niagara',
                                   frontCover=(resources.path('niagara.jpg'), 'Cover'),
                                   releaseTime='1971',
                                   trackTitle='Rolo le Baroudeur',
                                   lyricist=u'Étienne Roda-Gil')