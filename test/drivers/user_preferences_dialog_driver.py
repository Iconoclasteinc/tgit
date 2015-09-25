# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog

from ._screen_driver import ScreenDriver
from cute.matchers import named, with_buddy, showing_on_screen
from cute.widgets import window, QDialogDriver


def user_preferences_dialog(parent):
    return UserPreferencesDialogDriver(window(QDialog, named('user_preferences_dialog'), showing_on_screen()), parent.prober,
                                       parent.gesture_performer)


class UserPreferencesDialogDriver(QDialogDriver, ScreenDriver):
    def shows_preferences(self, preferences):
        if 'language' in preferences:
            self.shows_language(preferences['language'])

    def change_preferences(self, preferences):
        if 'language' in preferences:
            self.select_language(preferences['language'])

        self.ok()

    def shows_language(self, language):
        self.combobox(named('language')).has_current_text(language)

    def select_language(self, language):
        label = self.label(with_buddy(named('language')))
        label.is_showing_on_screen()
        self.combobox(named('language')).select_option(language)
