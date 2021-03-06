# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog

from cute.matchers import named, with_buddy, showing_on_screen
from cute.widgets import window, QDialogDriver
from ._screen_driver import ScreenDriver


def user_preferences_dialog(parent):
    return UserPreferencesDialogDriver(window(QDialog, named('settings_dialog'), showing_on_screen()), parent.prober,
                                       parent.gesture_performer)


class UserPreferencesDialogDriver(QDialogDriver, ScreenDriver):
    def shows_preferences(self, preferences):
        if 'language' in preferences:
            self.shows_language(preferences['language'])

    def change_preferences(self, preferences):
        if 'language' in preferences:
            self.select_language(preferences['language'])

        self.click_ok()

    def shows_language(self, language):
        self.language.has_current_text(language)

    def select_language(self, language):
        self.language_caption.is_showing_on_screen()
        self.language.select_option(language)

    @property
    def language_caption(self):
        return self.label(with_buddy(named('_language')))

    @property
    def language(self):
        return self.combobox(named('_language'))
