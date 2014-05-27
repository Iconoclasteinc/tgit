# -*- coding: utf-8 -*-
from PyQt4.QtGui import QWidget, QHBoxLayout, QLabel

from test.cute.finders import WidgetIdentity
from test.cute.matchers import named
from test.cute.probes import ValueMatcherProbe
from test.drivers.album_screen_driver import AlbumScreenDriver
from test.integration.ui.views import ViewTest
from test.util import resources

from tgit.ui.views.album_screen import AlbumScreen
from tgit.util import fs


def loadImage(name):
    return fs.readContent(resources.path(name))


def aPage(name):
    page = QWidget()
    page.setObjectName(name)
    layout = QHBoxLayout()
    layout.addWidget(QLabel(name))
    page.setLayout(layout)
    return page


class AlbumScreenTest(ViewTest):
    def setUp(self):
        super(AlbumScreenTest, self).setUp()
        self.view = AlbumScreen()
        self.show(self.view)
        self.driver = self.createDriverFor(self.view)

    def createDriverFor(self, widget):
        return AlbumScreenDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testHasButtonsInitiallyDisabled(self):
        self.driver.hasDisabledPreviousPageButton()
        self.driver.hasDisabledSaveButton()
        self.driver.hasDisabledNextPageButton()

    def testSignalsWhenSaveButtonClicked(self):
        recordAlbumSignal = ValueMatcherProbe('record album')
        self.view.bind(recordAlbum=recordAlbumSignal.received)
        self.view.allowSaves()
        self.driver.save()
        self.driver.check(recordAlbumSignal)

    def testAcceptsAppendingNewPages(self):
        self.view.appendPage(aPage('page #0'))
        self.view.appendPage(aPage('page #1'))
        self.view.appendPage(aPage('page #2'))

        self.driver.showsPage(named('page #0'))
        self.view.toPage(1)
        self.driver.showsPage(named('page #1'))
        self.view.toPage(2)
        self.driver.showsPage(named('page #2'))

    def testSupportsPageRemoval(self):
        self.view.appendPage(aPage('page #0'))
        self.view.appendPage(aPage('page #1'))
        self.view.appendPage(aPage('page #2'))
        self.view.appendPage(aPage('page #3'))
        self.view.appendPage(aPage('page #4'))

        self.view.removePage(0)
        self.driver.showsPage(named('page #1'))
        self.view.removePage(1)
        self.view.toPage(2)
        self.driver.showsPage(named('page #4'))
        self.view.removePage(2)
        self.driver.showsPage(named('page #3'))

    def testOffersBackAndForthNavigationBetweenPages(self):
        self.view.appendPage(aPage('page #0'))
        self.view.appendPage(aPage('page #1'))
        self.view.appendPage(aPage('page #2'))

        self.driver.nextPage()
        self.driver.showsPage(named('page #1'))
        self.driver.nextPage()
        self.driver.showsPage(named('page #2'))
        self.driver.previousPage()
        self.driver.showsPage(named('page #1'))
        self.driver.previousPage()
        self.driver.showsPage(named('page #0'))
        self.driver.nextPage()
        self.driver.showsPage(named('page #1'))

    def testDisablesNextPageButtonOnLastPage(self):
        self.view.appendPage(aPage('page #0'))
        self.view.appendPage(aPage('page #1'))
        self.view.toPage(1)
        self.driver.hasDisabledNextPageButton()
        self.view.toPage(0)
        self.driver.hasEnabledNextPageButton()
        self.view.removePage(1)
        self.driver.hasDisabledNextPageButton()

    def testDisablesPreviousPageButtonOnFirstPage(self):
        self.view.appendPage(aPage('page #0'))
        self.view.appendPage(aPage('page #1'))
        self.driver.hasDisabledPreviousPageButton()
        self.view.toPage(1)
        self.driver.hasEnabledPreviousPageButton()
        self.view.removePage(0)
        self.driver.hasDisabledPreviousPageButton()

    def testSupportsInsertingNewPages(self):
        self.view.appendPage(aPage('page #0'))
        self.view.appendPage(aPage('page #1'))
        self.view.appendPage(aPage('page #3'))
        self.driver.nextPage()
        self.driver.showsPage(named('page #1'))

        self.view.insertPage(aPage('page #2'), 2)
        self.driver.nextPage()
        self.driver.showsPage(named('page #2'))

        self.driver.nextPage()
        self.driver.showsPage(named('page #3'))

    def testDisablesOrEnablesSaveButtonOnDemand(self):
        self.view.allowSaves()
        self.driver.hasEnabledSaveButton()
        self.view.allowSaves(False)
        self.driver.hasDisabledSaveButton()
        self.view.allowSaves()
        self.driver.hasEnabledSaveButton()

    def testIncludesHelpLink(self):
        self.driver.linksHelpTo("http://tagtamusique.com/2013/12/03/tgit_style_guide/")

    def testIncludesFeatureRequestLink(self):
        self.driver.linksFeatureRequestTo("mailto:iconoclastejr@gmail.com")