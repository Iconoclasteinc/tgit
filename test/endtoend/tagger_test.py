# -*- coding: utf-8 -*-

import unittest

from test.util import resources, fakes
from test.endtoend.application_runner import ApplicationRunner

from tgit.util import fs


class TaggerTest(unittest.TestCase):
    def setUp(self):
        self.application = ApplicationRunner()
        self.metadataContainer = fakes.metadataContainer()
        self.application.start()

    def tearDown(self):
        self.application.stop()
        self.metadataContainer.delete()

    def testCreatesAndTagsANewAlbum(self):
        maPreference = self.metadataContainer.add(
            trackTitle=u'Ma préférence',
            releaseName='Jaloux',
            frontCover=('image/jpeg', 'Cover', fs.readContent(resources.path('jaloux.jpg'))),
            leadPerformer='Julien Clerc',
            labelName='EMI',
            releaseTime='1978')
        faisMoiUnePlace = self.metadataContainer.add(
            trackTitle='Fais moi une place',
            releaseName='Fais moi une place',
            frontCover=('image/jpeg', 'Cover', fs.readContent(resources.path('une-place.jpg'))),
            labelName='Virgin',
            releaseTime='1990',
            upc='3268440307258')
        rolo = self.metadataContainer.add(
            trackTitle='Rolo le Baroudeur',
            releaseName='Niagara',
            frontCover=('image/jpeg', 'Cover', fs.readContent(resources.path('niagara.jpg'))),
            releaseTime='1971',
            lyricist=u'Étienne Roda-Gil'
        )
        ceNestRien = self.metadataContainer.add(
            trackTitle="Ce n'est rien",
            releaseName='Niagara',
            frontCover=('image/jpeg', 'Cover', fs.readContent(resources.path('niagara.jpg'))),
            releaseTime='1971',
            lyricist=u'Étienne Roda-Gil')

        self.application.newAlbum(maPreference)
        self.application.addTrack(faisMoiUnePlace)
        self.application.addTrack(rolo)
        self.application.addTrack(ceNestRien)

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

        self.metadataContainer.contains(u'Julien Clerc - Ma préférence.mp3',
                                        frontCover=(resources.path('best-of.jpg'), 'Front Cover'),
                                        releaseName='Best Of',
                                        leadPerformer='Julien Clerc',
                                        labelName='EMI Music France',
                                        releaseTime='2009-04-06',
                                        trackTitle=u'Ma préférence',
                                        composer='Julien Clerc',
                                        lyricist='Jean-Loup Dabadie')
        self.metadataContainer.contains(u'Julien Clerc - Fais moi une place.mp3',
                                        frontCover=(resources.path('best-of.jpg'), 'Front Cover'),
                                        releaseName='Best Of',
                                        leadPerformer='Julien Clerc',
                                        labelName='EMI Music France',
                                        releaseTime='2009-04-06',
                                        trackTitle=u'Fais moi une place',
                                        composer='Julien Clerc',
                                        lyricist='Francoise Hardy')
        self.metadataContainer.contains(u"Julien Clerc - Ce n'est rien.mp3",
                                        frontCover=(resources.path('best-of.jpg'), 'Front Cover'),
                                        releaseName='Best Of',
                                        leadPerformer='Julien Clerc',
                                        labelName='EMI Music France',
                                        releaseTime='2009-04-06',
                                        trackTitle=u"Ce n'est rien",
                                        composer='Julien Clerc',
                                        lyricist=u'Étienne Roda-Gil')