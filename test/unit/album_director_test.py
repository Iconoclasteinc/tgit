# -*- coding: utf-8 -*-
import unittest
from hamcrest import assert_that, equal_to
from test.util import builders as build

from tgit import album_director
from tgit.album_director import Snapshot


class AlbumDirectorTest(unittest.TestCase):
    def testUpdatesTrackMetadata(self):
        changes = Snapshot()
        changes.trackTitle = 'Title'
        changes.leadPerformer = 'Artist'
        changes.versionInfo = 'Version'
        changes.featuredGuest = 'Featuring'
        changes.lyricist = 'Lyricist'
        changes.composer = 'Composer'
        changes.publisher = 'Publisher'
        changes.isrc = 'ZZZ123456789'
        changes.tags = 'Tags'
        changes.lyrics = 'Lyrics\nLyrics\n...'
        changes.language = 'und'

        track = build.track()
        album_director.updateTrack(track, changes)

        assert_that(track.trackTitle, equal_to('Title'), 'track title')
        assert_that(track.leadPerformer, equal_to('Artist'), 'lead performer')
        assert_that(track.versionInfo, equal_to('Version'), 'version info')
        assert_that(track.featuredGuest, equal_to('Featuring'), 'featured guest')
        assert_that(track.lyricist, equal_to('Lyricist'), 'lyricist')
        assert_that(track.composer, equal_to('Composer'), 'composer')
        assert_that(track.publisher, equal_to('Publisher'), 'publisher')
        assert_that(track.isrc, equal_to('ZZZ123456789'), 'isrc')
        assert_that(track.tags, equal_to('Tags'), 'tags')
        assert_that(track.lyrics, equal_to('Lyrics\nLyrics\n...'), 'lyrics')
        assert_that(track.language, equal_to('und'), 'language')