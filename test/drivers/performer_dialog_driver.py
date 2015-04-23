# -*- coding: utf-8 -*-

from test.cute.matchers import named, withText
from test.drivers import BaseDriver


class PerformerDialogDriver(BaseDriver):
    def addPerformerRow(self):
        self.button(withText('ADD A PERFORMER')).click()

    def removePerformer(self, index):
        self.button(named('remove-performer-%(index)i' % locals())).click()

    def showsOkButton(self, disabled=False):
        self.button(withText('&OK')).is_disabled(disabled)

    def changePerformerName(self, name, index):
        self.lineEdit(named('performer-%(index)i' % locals())).replaceAllText(name)

    def changeInstrument(self, instrument, index):
        self.lineEdit(named('instrument-%(index)i' % locals())).replaceAllText(instrument)

    def ok(self):
        self.button(withText('OK')).click()

    def cancel(self):
        self.button(withText('Cancel')).click()
