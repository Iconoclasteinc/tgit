from PyQt4.QtGui import QDialog

from test.cute.matchers import named, withText, showingOnScreen
from test.cute.widgets import window
from test.drivers.__base import BaseDriver


def performerDialog(parent):
    return PerformerDialogDriver(window(QDialog, named('performer-dialog'), showingOnScreen()), parent.prober,
                                 parent.gesturePerformer)


class PerformerDialogDriver(BaseDriver):
    def showsOkButton(self, disabled=False):
        self.button(withText('&OK')).isDisabled(disabled)

    def changePerformerName(self, name):
        self.lineEdit(named('performer')).changeText(name)

    def changeInstrument(self, instrument):
        self.lineEdit(named('instrument')).changeText(instrument)

    def ok(self):
        self.button(withText('&OK')).click()

    def cancel(self):
        self.button(withText('&Cancel')).click()
