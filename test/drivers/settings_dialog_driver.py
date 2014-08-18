from PyQt4.QtGui import QComboBox, QAbstractButton, QDialog, QLabel
from test.cute.matchers import named, withText, withBuddy
from test.cute.widgets import WidgetDriver, ComboBoxDriver, ButtonDriver, LabelDriver, window


def settingsDialog(parent):
    return SettingsDialogDriver(window(QDialog, named('settings-dialog')), parent.prober, parent.gesturePerformer)


class SettingsDialogDriver(WidgetDriver):
    def showsSettings(self, settings):
        if 'language' in settings:
            self.showsLanguage(settings['language'])

    def changeSettings(self, settings):
        if 'language' in settings:
            self.changeLanguage(settings['language'])

    def showsLanguage(self, language):
        self._combo(named('language')).hasCurrentText(language)

    def changeLanguage(self, language):
        label = self._label(withBuddy(named('language')))
        label.isShowingOnScreen()
        self._combo(named('language')).selectOption(language)
        self.ok()

    def ok(self):
        self._button(withText('OK')).click()

    def cancel(self):
        self._button(withText('Cancel')).click()

    def _combo(self, matching):
        return ComboBoxDriver.findSingle(self, QComboBox, matching)

    def _button(self, matching):
        return ButtonDriver.findSingle(self, QAbstractButton, matching)

    def _label(self, matching):
        return LabelDriver.findSingle(self, QLabel, matching)
