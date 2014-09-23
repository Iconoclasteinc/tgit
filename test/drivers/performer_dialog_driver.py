from PyQt4.QtGui import QDialog

from test.cute.matchers import named, withText, showingOnScreen
from test.cute.widgets import window
from test.drivers.__base import BaseDriver


class PerformerDialogDriver(BaseDriver):
    def addPerformerRow(self):
        self.button(withText('ADD A PERFORMER')).click()

    def showsOkButton(self, disabled=False):
        self.button(withText('&OK')).isDisabled(disabled)

    def changePerformerName(self, name, index):
        self.lineEdit(named('performer-%(index)i' % locals())).replaceAllText(name)

    def changeInstrument(self, instrument, index):
        self.lineEdit(named('instrument-%(index)i' % locals())).replaceAllText(instrument)

    def ok(self):
        self.button(withText('&OK')).click()

    def cancel(self):
        self.button(withText('&Cancel')).click()
