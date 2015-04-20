# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QAbstractButton

from test.cute import matchers as match
from test.cute.matchers import showingOnScreen, withText
from test.cute.widgets import MainWindowDriver, WidgetDriver, ButtonDriver
from test.drivers.export_as_dialog_driver import exportAsDialog
from test.drivers.menu_bar_driver import menuBar
from test.drivers.album_screen_driver import album_screen
from test.drivers.settings_dialog_driver import settingsDialog
from test.drivers.track_selection_dialog_driver import track_selection_dialog
from test.drivers.welcome_screen_driver import welcome_screen


def restartMessage(parent):
    return WidgetDriver.findSingle(parent, QDialog, match.named('restart-message'), showingOnScreen())


class TaggerDriver(MainWindowDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TaggerDriver, self).__init__(selector, prober, gesturePerformer)

    def enterAudioFile(self, filename):
        track_selection_dialog(self).enter_track(filename)

    def select_audio_files(self, of_type, *paths):
        track_selection_dialog(self).select_tracks(of_type, *paths)

    def cancelSelection(self):
        track_selection_dialog(self).cancel()

    def create_album(self):
        welcome_screen(self).new_album()
        self.shows_album_screen()

    def showsWelcomeScreen(self):
        welcome_screen(self).isShowingOnScreen()

    def shows_album_screen(self):
        album_screen(self).isShowingOnScreen()

    def showsExportAsDialog(self):
        exportAsDialog(self).isShowingOnScreen()

    def removeTrack(self, title):
        album_screen(self).removeTrack(title)

    def moveTrack(self, title, to):
        album_screen(self).moveTrack(title, to)

    # todo have a quick navigation button
    def next(self):
        album_screen(self).nextPage()

    def showsAlbumContains(self, *tracks):
        album_screen(self).showsAlbumContains(*tracks)

    def shows_album_metadata(self, **tags):
        album_screen(self).shows_album_metadata(**tags)

    def edit_album_metadata(self, **tags):
        album_screen(self).edit_album_metadata(**tags)

    def showsTrackMetadata(self, **tags):
        album_screen(self).showsTrackMetadata(**tags)

    def editTrackMetadata(self, **tags):
        album_screen(self).editTrackMetadata(**tags)

    def save_album(self):
        album_screen(self).save()

    def change_settings(self, **settings):
        menuBar(self).settings()
        settingsDialog(self).changeSettings(settings)
        self.acknowledge()

    def hasSettings(self, **settings):
        dialog = menuBar(self).settings()
        try:
            dialog.showsSettings(settings)
        finally:
            dialog.close()

    def acknowledge(self):
        message = restartMessage(self)
        ok = ButtonDriver.findSingle(message, QAbstractButton, withText('OK'))
        ok.click()