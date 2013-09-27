# -*- coding: utf-8 -*-

import unittest
from flexmock import flexmock

import use_sip_api_v2 as sipApi
sipApi.useVersion(sipApi.VERSION_2)
# todo Settle on a practice for importing Qt classes
from PyQt4.Qt import QApplication

from tests.cute.events import MainEventLoop
from tests.cute.prober import EventProcessingProber
from tests.cute.robot import Robot
from tests.cute.finders import WidgetSelector
from tests.drivers.album_panel_driver import AlbumPanelDriver
from tests.util import resources

from tgit.ui.album_panel import AlbumPanel
# todo consider moving all ui constants to the same module (ui?)
from tgit.ui import album_panel as ui


def buildTrack(**tags):
    defaults = dict(releaseName=None,
                    frontCoverPicture=(None, None),
                    leadPerformer=None,
                    releaseDate=None,
                    upc=None)
    return flexmock(**dict(defaults.items() + tags.items()))


END_OF_TEST_PAUSE = 500


# todo Extract an abstract base class for ui integration tests
class AlbumPanelTest(unittest.TestCase):
    # todo make this configurable through an environment variable to speed up build
    # on demand

    def setUp(self):
        self.app = QApplication([])
        self.prober = EventProcessingProber(timeoutInMs=1000)
        self.gesturePerformer = Robot()
        self.albumPanel = AlbumPanel()
        self.view(self.albumPanel)
        self.driver = self.createDriverFor(self.albumPanel)

    def createDriverFor(self, widget):
        return AlbumPanelDriver(self.selectorFor(widget), self.prober, self.gesturePerformer)

    def view(self, widget):
        widget.show()
        widget.raise_()

    def pause(self, ms):
        MainEventLoop.processEventsFor(ms)

    def tearDown(self):
        self.pause(END_OF_TEST_PAUSE)
        self.driver.close()
        del self.driver
        del self.app

    def testCanShow(self):
        pass

    def testDisplaysFrontCoverScaledToPictureDisplayArea(self):
        frontCover = ('image/jpeg', readContent(resources.path("front-cover.jpg")))
        track = buildTrack(frontCoverPicture=frontCover)
        self.albumPanel.trackSelected(track)
        self.driver.displaysFrontCoverPictureWithSize(*ui.FRONT_COVER_DISPLAY_SIZE)

    @unittest.skip("todo")
    def testLetsUserSelectAFrontCoverPicture(self):
        raise AssertionError("Not yet implemented")

    def testDisplaysReleaseName(self):
        track = buildTrack(releaseName='Release Name')
        self.albumPanel.trackSelected(track)
        self.driver.showsReleaseName('Release Name')

    def testDisplaysLeadPerformer(self):
        track = buildTrack(leadPerformer='Lead Performer')
        self.albumPanel.trackSelected(track)
        self.driver.showsLeadPerformer('Lead Performer')

    def selectorFor(self, widget):
        # todo Move to finders.py
        class WidgetIdentity(WidgetSelector):
            def __init__(self, widget):
                self._widget = widget

            def test(self):
                pass

            def widgets(self):
                return self._widget,

            def widget(self):
                return self._widget

            def isSatisfied(self):
                return True

            def describeTo(self, description):
                description.append_text("the exact ") \
                    .append_text(type(self._widget).__name__) \
                    .append_text(" '%s'" % repr(self._widget))

            def describeFailureTo(self, description):
                self.describeTo(description)

        return WidgetIdentity(widget)


import mimetypes

from hamcrest.core import equal_to
from hamcrest.library import contains, has_length

# todo move to a file related utilities module
def readContent(filename):
    return open(filename, "rb").read()


# todo move to a file related utilities module
def guessMimeType(filename):
    return mimetypes.guess_type(filename)[0]


# todo move to a matchers module
def samePictureAs(filename):
    return contains(equal_to(guessMimeType(filename)),
                    has_length(len(readContent(filename))))


