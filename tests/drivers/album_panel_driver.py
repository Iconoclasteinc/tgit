# -*- coding: utf-8 -*-

import os
from PyQt4.QtGui import QLabel, QLineEdit, QPushButton, QFileDialog

from tests.cute.matchers import named, withBuddy, withPixmapHeight, withPixmapWidth
from tests.cute.widgets import (WidgetDriver, LabelDriver, LineEditDriver, AbstractButtonDriver, 
                                FileDialogDriver)

import tgit.ui.album_panel as ui


class AlbumPanelDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(AlbumPanelDriver, self).__init__(selector, prober, gesturePerformer)

    def displaysFrontCoverPictureWithSize(self, width, height):
        label = LabelDriver.find(self, QLabel, named(ui.FRONT_COVER_PICTURE_NAME))
        label.isShowingOnScreen()
        label.hasPixmap(withPixmapHeight(height))
        label.hasPixmap(withPixmapWidth(width))
        
    def changeFrontCoverPicture(self, filename):
        self._openSelectPictureDialog()
        self._selectPicture(filename)
        self.displaysFrontCoverPictureWithSize(*ui.FRONT_COVER_DISPLAY_SIZE)

    def _openSelectPictureDialog(self):
        button = AbstractButtonDriver.find(self, QPushButton, named(ui.SELECT_PICTURE_BUTTON_NAME))
        button.click()

    def _selectPicture(self, filename):
        dialog = FileDialogDriver.find(self, QFileDialog, named(ui.SELECT_PICTURE_DIALOG_NAME))
        dialog.navigateToDir(os.path.dirname(filename))
        dialog.selectFile(os.path.basename(filename))
        dialog.accept()

    def showsReleaseName(self, name):
        label = LabelDriver.find(self, QLabel, withBuddy(named(ui.RELEASE_NAME_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.find(self, QLineEdit, named(ui.RELEASE_NAME_NAME))
        edit.hasText(name)
        
    def changeReleaseName(self, name):
        edit = LineEditDriver.find(self, QLineEdit, named(ui.RELEASE_NAME_NAME))
        edit.replaceAllText(name)

    def showsLeadPerformer(self, name):
        label = LabelDriver.find(self, QLabel, withBuddy(named(ui.LEAD_PERFORMER_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.find(self, QLineEdit, named(ui.LEAD_PERFORMER_NAME))
        edit.hasText(name)

    def changeLeadPerformer(self, name):
        edit = LineEditDriver.find(self, QLineEdit, named(ui.LEAD_PERFORMER_NAME))
        edit.replaceAllText(name)

    def showsReleaseDate(self, date):
        label = LabelDriver.find(self, QLabel, withBuddy(named(ui.RELEASE_DATE_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.find(self, QLineEdit, named(ui.RELEASE_DATE_NAME))
        edit.hasText(date)

    def changeReleaseDate(self, date):
        edit = LineEditDriver.find(self, QLineEdit, named(ui.RELEASE_DATE_NAME))
        edit.replaceAllText(date)

    def showsUpc(self, code):
        label = LabelDriver.find(self, QLabel, withBuddy(named(ui.UPC_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.find(self, QLineEdit, named(ui.UPC_NAME))
        edit.hasText(code)

    def changeUpc(self, code):
        edit = LineEditDriver.find(self, QLineEdit, named(ui.UPC_NAME))
        edit.replaceAllText(code)