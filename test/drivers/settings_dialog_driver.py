# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QComboBox, QAbstractButton, QDialog, QLabel

from cute.matchers import named, with_text, with_buddy, showing_on_screen
from cute.widgets import WidgetDriver, ComboBoxDriver, ButtonDriver, LabelDriver, window


def settings_dialog(parent):
    return SettingsDialogDriver(window(QDialog, named('settings-dialog'), showing_on_screen()), parent.prober,
                                parent.gesture_performer)


class SettingsDialogDriver(WidgetDriver):
    def showsSettings(self, settings):
        if 'language' in settings:
            self.showsLanguage(settings['language'])

    def changeSettings(self, settings):
        if 'language' in settings:
            self.changeLanguage(settings['language'])

    def showsLanguage(self, language):
        self._combo(named('language')).has_current_text(language)

    def changeLanguage(self, language):
        label = self._label(with_buddy(named('language')))
        label.is_showing_on_screen()
        self._combo(named('language')).select_option(language)
        self.ok()

    def ok(self):
        self._button(with_text('OK')).click()

    def cancel(self):
        self._button(with_text('Cancel')).click()

    def _combo(self, matching):
        return ComboBoxDriver.find_single(self, QComboBox, matching)

    def _button(self, matching):
        return ButtonDriver.find_single(self, QAbstractButton, matching)

    def _label(self, matching):
        return LabelDriver.find_single(self, QLabel, matching)
