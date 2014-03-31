# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences
import tgit.use_sip_api_v2

from datetime import timedelta
import unittest

from flexmock import flexmock
from hamcrest import assert_that, equal_to, is_, has_property, contains

from PyQt4.QtCore import Qt, QModelIndex

from test.util import builders as build
from test.util import fakes

from tgit.ui import display
from tgit.ui.views.album_composition_model import AlbumCompositionModel, Columns, Row


QModelIndex.__str__ = lambda self: '(%s, %s)' % (self.row(), self.column())


def anInvalidIndex():
    return QModelIndex()


class StubAlbumCompositionModel(AlbumCompositionModel):
    inserting = False
    removing = False

    def beginInsertRows(self, index, position, rows):
        self.inserting = True

    def endInsertRows(self):
        self.inserting = False

    def beginRemoveRows(self, index, position, rows):
        self.removing = True

    def endRemoveRows(self):
        self.removing = False


class RowTest(unittest.TestCase):
    def testHoldsTrackDetails(self):
        track = build.track(trackTitle='Song',
                            leadPerformer='Artist',
                            bitrate=192000,
                            duration=100)
        album = build.album(releaseName='Album')

        row = Row(album, track)

        assert_that(row.trackTitle, equal_to('Song'), 'track title')
        assert_that(row.leadPerformer(), equal_to('Artist'), 'lead performer')
        assert_that(row.releaseName(), equal_to('Album'), 'release name')
        assert_that(row.bitrate(), equal_to(192000), 'bitrate')
        assert_that(row.duration(), equal_to(100), 'duration')
        assert_that(row.playing(), equal_to(False), 'playing')

    def testSignalsRowChangedWhenTrackStateChanges(self):
        track = build.track()
        row = Row(build.album(), track)
        listener = flexmock()
        row.rowChanged.connect(lambda row: listener.rowChanged(row))
        listener.should_receive('rowChanged').with_args(row).once()
        row.trackStateChanged(track)

    def testMovesTrackInAlbum(self):
        album = build.album(tracks=[
            build.track(trackTitle='Track #1'),
            build.track(trackTitle='Track #2')])
        row = Row(album, album.tracks[0])
        row.moveTo(1)

        assert_that(album.tracks, contains(
            has_property('trackTitle', 'Track #2'),
            has_property('trackTitle', 'Track #1')), 'album tracks')

    def testStartsAndStopsPlayingTrack(self):
        player = flexmock(fakes.audioPlayer())

        album = build.album(tracks=[build.track(filename='track.mp3')])
        track = album.tracks[0]
        row = Row(album, track)

        player.should_receive('play').with_args('track.mp3').once()
        row.play(player)
        assert_that(row.playing(), is_(True), 'playing once started')

        player.should_receive('stop').once()
        row.stop(player)
        assert_that(row.playing(), is_(False), 'playing once stopped')

    def testSignalsRowChangedWhenTrackHasStartedPlaying(self):
        album = build.album()
        track = build.track(filename='track.mp3')
        other = build.track(filename='other.mp3')
        album.addTrack(track)
        album.addTrack(other)

        row = Row(album, track, False)
        listener = flexmock()
        row.rowChanged.connect(lambda row: listener.rowChanged(row))

        listener.should_receive('rowChanged').never()
        row.started('other.mp3')
        assert_that(row.playing(), is_(False), 'playing when not started')

        listener.should_receive('rowChanged').with_args(row).once()
        row.started('track.mp3')
        assert_that(row.playing(), is_(True), 'playing once started')

    def testSignalsRowChangedWhenTrackHasStoppedPlaying(self):
        album = build.album()
        track = build.track(filename='track.mp3')
        other = build.track(filename='other.mp3')
        album.addTrack(track)
        album.addTrack(other)

        row = Row(album, track, True)
        listener = flexmock()
        row.rowChanged.connect(lambda row: listener.rowChanged(row))

        listener.should_receive('rowChanged').never()
        row.stopped('other.mp3')
        assert_that(row.playing(), is_(True), 'playing when not stopped')

        listener.should_receive('rowChanged').with_args(row).once()
        row.stopped('track.mp3')
        assert_that(row.playing(), is_(False), 'playing once stopped')


class ColumnsTest(unittest.TestCase):
    def testFormatsRowForDisplay(self):
        track = build.track(trackTitle='Song',
                            leadPerformer='Artist',
                            bitrate=192000,
                            duration=timedelta(minutes=4, seconds=37).total_seconds())
        album = build.album(releaseName='Album')

        row = Row(album, track, True)
        assert_that(Columns.trackTitle.value(row), equal_to('Song'), 'track title')
        assert_that(Columns.leadPerformer.value(row), equal_to('Artist'), 'lead performer')
        assert_that(Columns.releaseName.value(row), equal_to('Album'), 'release name')
        assert_that(Columns.bitrate.value(row), equal_to('192 kbps'), 'bitrate')
        assert_that(Columns.duration.value(row), equal_to('04:37'), 'duration')
        assert_that(Columns.play.value(row), equal_to(True), 'playing')
        assert_that(Columns.remove.value(row), is_(None), 'remove')


class AlbumCompositionModelTest(unittest.TestCase):
    def setUp(self):
        self.album = build.album()
        self.player = flexmock(fakes.audioPlayer())
        self.model = flexmock(StubAlbumCompositionModel(self.album, self.player))

    def testHasEnoughColumns(self):
        assert_that(self.model.columnCount(), equal_to(len(Columns)), 'column count')

    def testSetsUpColumnHeadings(self):
        for index, column in enumerate(Columns):
            assert_that(self.model.headerData(index, Qt.Horizontal), equal_to(column.name),
                        'name of column %d' % index)

    def testIsInitiallyEmpty(self):
        assert_that(self.model.rowCount(), equal_to(0), 'initial row count')

    def testHasEnoughRowsForAllTracksInAlbum(self):
        totalTracks = 10
        for i in range(totalTracks):
            self.album.addTrack(build.track())

        assert_that(self.model.rowCount(), equal_to(totalTracks), 'row count')

    def testNumbersRows(self):
        totalTracks = 10
        for i in range(totalTracks):
            self.album.addTrack(build.track())

        for index in range(self.model.rowCount()):
            assert_that(self.model.headerData(index, Qt.Vertical), equal_to(str(index + 1)),
                        'name of row %d' % index)

    def testReturnsInvalidHeaderForUnsupportedRoles(self):
        assert_that(self.model.headerData(0, Qt.Horizontal, Qt.UserRole), is_(None))

    def testAddsRowForNewTrackAndSignalsInsertion(self):
        self.model.should_call('beginInsertRows').with_args(anInvalidIndex(), 0, 0)\
            .once().when(lambda: not self.model.inserting).once()
        self.model.should_call('endInsertRows').once().when(lambda: self.model.inserting)

        track = build.track(trackTitle='Song')
        self.album.addTrack(track)
        self.assertRowMatchesTrack(0, track)

    def testDisplaysTrackDetailsInColumns(self):
        self.album.releaseName = 'Album'
        track = build.track(trackTitle='Song',
                            leadPerformer='Artist',
                            duration=timedelta(minutes=3, seconds=56).total_seconds(),
                            bitrate=192000)
        self.album.addTrack(track)
        self.assertRowMatchesTrack(0, track)
        self.assertRowMatchesAlbum(0, self.album)

    def testDisplaysTracksInAdditionOrder(self):
        track1 = build.track(trackTitle='Track #1')
        track2 = build.track(trackTitle='Track #2')
        track3 = build.track(trackTitle='Track #3')

        self.album.addTrack(track1)
        self.album.addTrack(track2)
        self.album.addTrack(track3)
        self.assertRowMatchesTrack(0, track1)
        self.assertRowMatchesTrack(1, track2)
        self.assertRowMatchesTrack(2, track3)

    def testSignalsWhenTrackStateHasChangedAndUpdatesCorrectRow(self):
        self.album.addTrack(build.track(trackTitle='Track #1'))
        track = build.track()
        self.album.addTrack(track)

        modelListener = flexmock()
        self.model.dataChanged.connect(lambda start, end: modelListener.dataChanged(start, end))
        modelListener.should_receive('dataChanged').with_args(self.model.index(1, 0),
                                                              self.model.index(1, 6)).once()

        track.trackTitle = 'Track #2'
        self.assertRowMatchesTrack(1, track)

    def testSignalsWhenAlbumStateHasChangedAndUpdatesAllRows(self):
        self.album.addTrack(build.track())
        self.album.addTrack(build.track())
        self.album.addTrack(build.track())

        modelListener = flexmock()
        self.model.dataChanged.connect(lambda start, end: modelListener.dataChanged(start, end))
        # album has changed
        modelListener.should_receive('dataChanged').with_args(self.model.index(0, 2),
                                                              self.model.index(2, 2)).once()

        # each track in album also triggers a data change
        # todo change this behavior. What do we want to see?
        modelListener.should_receive('dataChanged').with_args(self.model.index(0, 0),
                                                              self.model.index(0, 6)).once()
        modelListener.should_receive('dataChanged').with_args(self.model.index(1, 0),
                                                              self.model.index(1, 6)).once()
        modelListener.should_receive('dataChanged').with_args(self.model.index(2, 0),
                                                              self.model.index(2, 6)).once()

        self.album.releaseName = 'Album'
        self.album.leadPerfomer = 'Artist'

        for row in range(self.model.rowCount()):
            self.assertRowMatchesAlbum(row, self.album)

    def testRemovesRowForDroppedTrackAndSignalsRemoval(self):
        self.model.should_call('beginRemoveRows').with_args(anInvalidIndex(), 0, 0)\
            .once().when(lambda: not self.model.removing).once()
        self.model.should_call('endRemoveRows').once().when(lambda: self.model.removing)

        track = build.track()
        self.album.addTrack(track)
        assert_that(self.model.rowCount(), equal_to(1), 'row count before removal')
        self.album.removeTrack(track)
        assert_that(self.model.rowCount(), equal_to(0), 'row count after removal')

    def testNoLongerSignalsTrackStateChangedWhenRowHasBeenRemoved(self):
        track = build.track()
        self.album.addTrack(track)
        self.album.removeTrack(track)

        modelListener = flexmock()
        self.model.dataChanged.connect(lambda start, end: modelListener.dataChanged(start, end))
        modelListener.should_receive('dataChanged').never()
        track.trackTitle = 'Track'

    def assertRowMatchesAlbum(self, row, album):
        self.assertCellDisplays(row, Columns.releaseName, album.releaseName)

    def assertRowMatchesTrack(self, row, track):
        self.assertCellDisplays(row, Columns.trackTitle, track.trackTitle)
        self.assertCellDisplays(row, Columns.leadPerformer, track.leadPerformer)
        if track.bitrate:
            self.assertCellDisplays(row, Columns.bitrate, '%d kbps' % display.inKbps(track.bitrate))
        if track.duration:
            self.assertCellDisplays(row, Columns.duration, display.asDuration(track.duration))

    def assertCellDisplays(self, row, column, value):
        assert_that(self.cellValue(column, row), equal_to(value), 'cell (%d, %d)' % (row, Columns.index(column)))

    def cellValue(self, column, row):
        return self.model.data(self.model.index(row, Columns.index(column)), Qt.DisplayRole)
