# -*- coding: utf-8 -*-

from cute.matchers import named, with_text
from test.drivers import BaseDriver


class PerformerDialogDriver(BaseDriver):
    def addPerformerRow(self):
        self.button(with_text('ADD A PERFORMER')).click()

    def removePerformer(self, index):
        self.button(named('remove-performer-%(index)i' % locals())).click()

    def showsOkButton(self, disabled=False):
        self.button(with_text('&OK')).is_disabled(disabled)

    def changePerformerName(self, name, index):
        self.lineEdit(named('performer-%(index)i' % locals())).replace_all_text(name)

    def changeInstrument(self, instrument, index):
        self.lineEdit(named('instrument-%(index)i' % locals())).replace_all_text(instrument)

    def ok(self):
        self.button(with_text('OK')).click()

    def cancel(self):
        self.button(with_text('Cancel')).click()
