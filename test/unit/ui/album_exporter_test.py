import os
import shutil
import tempfile
import unittest
from hamcrest import equal_to, assert_that
from test.util import builders as build
from tgit.ui.album_exporter import AlbumExporter
from tgit.util import fs


class StubExportFormat:
    def __init__(self):
        self.lines = []

    def willWriteLines(self, *lines):
        self.lines.extend(lines)

    def write(self, album, out):
        for line in self.lines:
            out.write(line)
            out.write('\n')


class ExportAsSelectorStub(object):
    def __init__(self):
        self.selectedDestination = None
        self.handlers = {}

    def __getattr__(self, item):
        if item not in self.handlers:
            raise AssertionError('No handler bound to event : ' + item)
        return self.handlers[item]

    def show(self):
        self.exportAs(self.selectedDestination)

    def bind(self, **handlers):
        self.handlers.update(handlers)


class AlbumExporterTest(unittest.TestCase):
    def setUp(self):
        self.album = build.album()
        self.format = StubExportFormat()
        self.exportSelector = ExportAsSelectorStub()
        self.exporter = AlbumExporter(self.album, self.format, self.exportSelector)
        self.exportFolder = createTempDir()

    def tearDown(self):
        deleteDir(self.exportFolder)

    def testFormatsAlbumToDestinationFile(self):
        destinationFile = os.path.join(self.exportFolder, 'album.csv')
        self.exportSelector.selectedDestination = destinationFile
        self.format.willWriteLines('track1', 'track2', 'track3')
        self.exporter.select()

        assert_that(contentOf(destinationFile), equal_to('track1\ntrack2\ntrack3\n'))


def contentOf(name):
    return fs.readContent(name)


def createTempDir():
    return tempfile.mkdtemp()


def deleteDir(path):
    shutil.rmtree(path)