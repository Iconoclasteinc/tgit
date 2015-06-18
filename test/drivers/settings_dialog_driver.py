# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog

from cute.matchers import named, with_buddy, showing_on_screen
from cute.widgets import window, QDialogDriver
from ._screen_driver import ScreenDriver


def settings_dialog(parent):
    return SettingsDialogDriver(window(QDialog, named('settings-dialog'), showing_on_screen()), parent.prober,
                                parent.gesture_performer)


class SettingsDialogDriver(QDialogDriver, ScreenDriver):
    def showsSettings(self, settings):
        if 'language' in settings:
            self.shows_language(settings['language'])

    def changeSettings(self, settings):
        if 'language' in settings:
            self.select_language(settings['language'])

        self.ok()

    def shows_language(self, language):
        self.combobox(named('language')).has_current_text(language)

    def select_language(self, language):
        label = self.label(with_buddy(named('language')))
        label.is_showing_on_screen()
        self.combobox(named('language')).select_option(language)
