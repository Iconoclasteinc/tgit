# -*- coding: utf-8 -*-

from hamcrest import assert_that, equal_to

from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe
from test.drivers.settings_dialog_driver import SettingsDialogDriver
from test.integration.ui import WidgetTest
from tgit.ui.settings_dialog import SettingsDialog


class SettingsDialogTest(WidgetTest):
    def setUp(self):
        super(SettingsDialogTest, self).setUp()
        self.dialog = SettingsDialog(transient=False)
        self.show(self.dialog)
        self.driver = self.createDriverFor(self.dialog)
        # It seems we need to give the dialog some time to show otherwise
        # we're clicking before it's on screen
        self.pause(200)

    def createDriverFor(self, widget):
        return SettingsDialogDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysUserPreferences(self):
        self.dialog.addLanguage('en', 'English')
        self.dialog.addLanguage('fr', 'French')
        self.dialog.display(language='fr')

        self.driver.showsLanguage('French')

    def testOffersSelectionOfAvailableLanguages(self):
        self.dialog.addLanguage('en', 'English')
        self.dialog.addLanguage('fr', 'French')
        assert_that(self.dialog.settings['language'], equal_to('en'), 'default language')

        # self.driver.showsLanguage('English')
        # self.driver.changeLanguage('French')
        # self.driver.showsLanguage('French')
        # assert_that(self.dialog.settings['language'], equal_to('fr'), 'selected language')

    def testSignalsWhenAccepted(self):
        self.dialog.addLanguage('en', 'English')

        acceptedSignal = ValueMatcherProbe("click on button 'OK'")
        self.dialog.accepted.connect(acceptedSignal.received)
        self.driver.ok()
        self.driver.check(acceptedSignal)

    def testSignalsWhenRejected(self):
        self.dialog.addLanguage('en', 'English')

        rejectedSignal = ValueMatcherProbe("click on button 'Cancel'")
        self.dialog.rejected.connect(rejectedSignal.received)
        self.driver.cancel()
        self.driver.check(rejectedSignal)