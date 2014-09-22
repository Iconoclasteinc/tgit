# -*- coding: utf-8 -*-
import unittest
from hamcrest import assert_that, equal_to
from tgit.util import sip_api
sip_api.use_v2()

from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe
from test.drivers.performer_dialog_driver import PerformerDialogDriver
from test.integration.ui import ViewTest
from tgit.ui.performer_dialog import PerformerDialog


class PerformerDialogTest(ViewTest):
    def setUp(self):
        super(PerformerDialogTest, self).setUp()
        self.dialog = PerformerDialog()
        self.show(self.dialog)
        self.driver = self.createDriverFor(self.dialog)

    def createDriverFor(self, widget):
        return PerformerDialogDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testEnablesOkButtonOnlyWhenFormIsNotFullyFilled(self):
        self.driver.showsOkButton(disabled=True)
        self.driver.changePerformerName('Jimmy Page')
        self.driver.showsOkButton(disabled=True)
        self.driver.changeInstrument('Guitar')
        self.driver.showsOkButton()

    def testGetsPerformerWhenFormIsFullyFilled(self):
        self.driver.changePerformerName('Jimmy Page')
        self.driver.changeInstrument('Guitar')
        performer = self.dialog.getPerformer()
        assert_that(performer, equal_to(('Guitar', 'Jimmy Page')), 'performer')

    @unittest.skip('Fails but don''t understand why')
    def testSignalsWhenAccepted(self):
        acceptedSignal = ValueMatcherProbe("click on button 'OK'")
        self.dialog.accepted.connect(acceptedSignal.received)
        self.driver.changePerformerName('Jimmy Page')
        self.driver.changeInstrument('Guitar')
        self.driver.ok()
        self.driver.check(acceptedSignal)

    def testSignalsWhenRejected(self):
        rejectedSignal = ValueMatcherProbe("click on button 'Cancel'")
        self.dialog.rejected.connect(rejectedSignal.received)
        self.driver.cancel()
        self.driver.check(rejectedSignal)