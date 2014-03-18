# -*- coding: utf-8 -*-
import os
import filecmp
import shutil
import tempfile

import unittest

from flexmock import flexmock
from hamcrest import assert_that, equal_to

from test.util import builders as build
from test.util import mp3_file
from tgit.track_library import TrackLibrary, TrackStorage, sanitize
from tgit.track import Track


class TrackStorageTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.original = mp3_file.make(to=self.tempdir).filename
        self.library = TrackStorage()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def testCopiesTrackFileToSameDirectoryUnderArtistAndTitleName(self):
        track = Track(self.original, build.metadata(leadPerformer='artist', trackTitle='title'))

        self.library.add(track)

        inLibrary = os.path.join(self.tempdir, 'artist - title.mp3')
        assert_that(os.path.exists(inLibrary), 'missing file ' + inLibrary)
        assert_that(filecmp.cmp(self.original, inLibrary, equal_to(True)), 'same file ' + inLibrary)

    def testSkipsCopyWhenFileAlreadyInLibrary(self):
        track = Track(self.original, build.metadata(leadPerformer='artist', trackTitle='title'))
        alreadyInLibrary = self.library.add(track)
        self.library.add(Track(alreadyInLibrary, track.metadata))

    def testReplacesInvalidCharactersForFileNamesWithUnderscores(self):
        assert_that(sanitize(u'1/2<3>4:5"6/7\\8?9*10|'), equal_to('1_2_3_4_5_6_7_8_9_10_'), 'sanitized name')

    def testStripsLeadingAndTrailingWhitespaceFromFileNames(self):
        assert_that(sanitize(u'  filename   '), equal_to('filename'), 'sanitized name')


class TrackLibraryTest(unittest.TestCase):
    def setUp(self):
        self.container = flexmock()
        self.storage = flexmock(add=lambda track: track.filename)
        self.library = TrackLibrary(self.container, self.storage)

    def testLoadsTrackMetadataFromContainer(self):
        metadata = build.metadata(trackTitle='Summertime',
                                  releaseName='My Favorite Things',
                                  images=[('image/jpeg', 'Front Cover', 'data')])

        self.container.should_receive('load').with_args('summertime.mp3').and_return(metadata)
        track = self.library.fetch('summertime.mp3')
        assert_that(track.metadata, equal_to(metadata), 'track metadata')

    def testSavesTrackMetadataToContainer(self):
        metadata = build.metadata(trackTitle='Summertime',
                                  releaseName='My Favorite Things',
                                  images=[('image/jpeg', 'Front Cover', 'data')])

        self.container.should_receive('save').with_args('summertime.mp3', metadata).once()
        self.library.store(Track('summertime.mp3', metadata))