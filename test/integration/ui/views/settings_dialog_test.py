# -*- coding: utf-8 -*-
from hamcrest import assert_that, equal_to
from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe

from test.drivers.settings_dialog_driver import SettingsDialogDriver
from test.integration.ui.views import ViewTest
from tgit.ui.views.settings_dialog import SettingsDialog


class SettingsDialogTest(ViewTest):
    def setUp(self):
        super(SettingsDialogTest, self).setUp()
        self.dialog = SettingsDialog()
        self.show(self.dialog)
        self.driver = self.createDriverFor(self.dialog)

    def createDriverFor(self, widget):
        return SettingsDialogDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysUserPreferences(self):
        self.dialog.addLanguage('English')
        self.dialog.addLanguage('French')
        self.dialog.display(language='French')

        self.driver.showsLanguage('French')

    def testOffersSelectionOfAvailableLanguages(self):
        self.dialog.addLanguage('English')
        self.dialog.addLanguage('French')
        assert_that(self.dialog.settings['language'], equal_to('English'), 'default language')

        self.driver.showsLanguage('English')
        self.driver.changeLanguage('French')
        self.driver.showsLanguage('French')
        assert_that(self.dialog.settings['language'], equal_to('French'), 'selected language')

    def testSignalsWhenAccepted(self):
        self.dialog.addLanguage('English')

        accepted = ValueMatcherProbe("click on button 'OK'")
        self.dialog.bind(ok=accepted.received)
        self.driver.ok()
        self.driver.check(accepted)

    def testSignalsWhenRejected(self):
        self.dialog.addLanguage('English')

        rejected = ValueMatcherProbe("click on button 'Cancel'")
        self.dialog.bind(cancel=rejected.received)
        self.driver.cancel()
        self.driver.check(rejected)