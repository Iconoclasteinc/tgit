# -*- coding: utf-8 -*-

from hamcrest import assert_that, equal_to

from cute.finders import WidgetIdentity
from cute.probes import ValueMatcherProbe
from test.drivers import PerformerDialogDriver
from test.integration.ui import WidgetTest
from tgit.ui.performer_dialog import PerformerDialog


class PerformerDialogTest(WidgetTest):
    def createDialog(self, performers=None):
        self.dialog = PerformerDialog(performers=performers, transient=False)
        self.show(self.dialog)
        self.pause(200)
        self.driver = self.createDriverFor(self.dialog)

    def createDriverFor(self, widget):
        return PerformerDialogDriver(WidgetIdentity(widget), self.prober, self.gesture_performer)

    def testAddsPerformers(self):
        self.createDialog()
        self.driver.changeInstrument('Guitar', index=0)
        self.driver.changePerformerName('Jimmy Page', index=0)
        self.driver.addPerformerRow()
        self.driver.changeInstrument('Vocals', index=1)
        self.driver.changePerformerName('Robert Plant', index=1)
        performers = self.dialog.getPerformers()
        assert_that(performers, equal_to([('Guitar', 'Jimmy Page'), ('Vocals', 'Robert Plant')]), 'performers')

    def testRemovesPerformers(self):
        self.createDialog([('Guitar', 'Jimmy Page'), ('Vocals', 'Robert Plant')])
        self.driver.removePerformer(1)
        performers = self.dialog.getPerformers()
        assert_that(performers, equal_to([('Guitar', 'Jimmy Page')]), 'performers')

    def testShowsPerformers(self):
        performers = [('Guitar', 'Jimmy Page'), ('Vocals', 'Robert Plant')]
        self.createDialog(performers=performers)

        rowsLayout = self.dialog.performersTable.layout()
        assert_that(rowsLayout.count(), equal_to(2), 'performer row count')

        self.checkPerformerForRow(0, 'Guitar', 'Jimmy Page')
        self.checkPerformerForRow(1, 'Vocals', 'Robert Plant')

    def testSignalsWhenAccepted(self):
        acceptedSignal = ValueMatcherProbe("click on button 'OK'")
        self.createDialog()
        self.dialog.accepted.connect(acceptedSignal.received)
        self.driver.ok()
        self.driver.check(acceptedSignal)

    def testSignalsWhenRejected(self):
        rejectedSignal = ValueMatcherProbe("click on button 'Cancel'")
        self.createDialog()
        self.dialog.rejected.connect(rejectedSignal.received)
        self.driver.cancel()
        self.driver.check(rejectedSignal)

    def checkPerformerForRow(self, rowIndex, instrument, name):
        row = self.dialog.performersTable.layout().itemAt(rowIndex).widget().layout()
        assert_that(row.itemAt(0).widget().text(), equal_to(instrument))
        assert_that(row.itemAt(1).widget().text(), equal_to(name))
