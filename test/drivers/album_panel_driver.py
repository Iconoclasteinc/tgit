# -*- coding: utf-8 -*-

import os
from PyQt4.QtGui import QLabel, QLineEdit, QPushButton, QFileDialog

import tgit.ui.album_panel as ui

from test.cute.matchers import named, withBuddy, withPixmapHeight, withPixmapWidth
from test.cute.widgets import (WidgetDriver, LabelDriver, LineEditDriver, AbstractButtonDriver,
                                FileDialogDriver)

UPC = 'upc'
RELEASE_DATE = 'releaseDate'
LEAD_PERFORMER = 'leadPerformer'
RELEASE_NAME = 'releaseName'
FRONT_COVER_EMBEDDED_TEXT = 'frontCoverEmbeddedText'
FRONT_COVER_PICTURE = 'frontCoverPicture'


class AlbumPanelDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(AlbumPanelDriver, self).__init__(selector, prober, gesturePerformer)

    def displaysFrontCoverPictureWithSize(self, width, height):
        label = LabelDriver.findIn(self, QLabel, named(ui.FRONT_COVER_PICTURE_NAME))
        label.isShowingOnScreen()
        label.hasPixmap(withPixmapHeight(height))
        label.hasPixmap(withPixmapWidth(width))
        
    def changeFrontCoverPicture(self, filename):
        self._openSelectPictureDialog()
        self._selectPicture(filename)
        self.displaysFrontCoverPictureWithSize(*ui.FRONT_COVER_DISPLAY_SIZE)

    def _openSelectPictureDialog(self):
        button = AbstractButtonDriver.findIn(self, QPushButton, named(ui.SELECT_PICTURE_BUTTON_NAME))
        button.click()

    def _selectPicture(self, filename):
        dialog = FileDialogDriver.findIn(self, QFileDialog, named(ui.SELECT_PICTURE_DIALOG_NAME))
        dialog.navigateToDir(os.path.dirname(filename))
        dialog.selectFile(os.path.basename(filename))
        dialog.accept()

    def showsMetadata(self, **tags):
        for tag, value in tags.iteritems():
            if tag == RELEASE_NAME:
                self.showsReleaseName(value)
            elif tag == LEAD_PERFORMER:
                self.showsLeadPerformer(value)
            elif tag == RELEASE_DATE:
                self.showsReleaseDate(value)
            elif tag == UPC:
                self.showsUpc(tags[UPC])
            else:
                AssertionError("Don't know how to verify <%s>" % tag)

    def showsReleaseName(self, name):
        label = LabelDriver.findIn(self, QLabel, withBuddy(named(ui.RELEASE_NAME_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.RELEASE_NAME_NAME))
        edit.hasText(name)
        
    def changeReleaseName(self, name):
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.RELEASE_NAME_NAME))
        edit.replaceAllText(name)

    def showsLeadPerformer(self, name):
        label = LabelDriver.findIn(self, QLabel, withBuddy(named(ui.LEAD_PERFORMER_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.LEAD_PERFORMER_NAME))
        edit.hasText(name)

    def changeMetadata(self, **tags):
        for tag, value in tags.iteritems():
            if tag == FRONT_COVER_PICTURE:
                self.changeFrontCoverPicture(value)
            elif tag == RELEASE_NAME:
                self.changeReleaseName(value)
            elif tag == LEAD_PERFORMER:
                self.changeLeadPerformer(value)
            elif tag == RELEASE_DATE:
                self.changeReleaseDate(value)
            elif tag == UPC:
                self.changeUpc(tags[UPC])
            else:
                AssertionError("Don't know how to edit <%s>" % tag)

    def changeLeadPerformer(self, name):
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.LEAD_PERFORMER_NAME))
        edit.replaceAllText(name)

    def showsReleaseDate(self, date):
        label = LabelDriver.findIn(self, QLabel, withBuddy(named(ui.RELEASE_DATE_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.RELEASE_DATE_NAME))
        edit.hasText(date)

    def changeReleaseDate(self, date):
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.RELEASE_DATE_NAME))
        edit.replaceAllText(date)

    def showsUpc(self, code):
        label = LabelDriver.findIn(self, QLabel, withBuddy(named(ui.UPC_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.UPC_NAME))
        edit.hasText(code)

    def changeUpc(self, code):
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.UPC_NAME))
        edit.replaceAllText(code)