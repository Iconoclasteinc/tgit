from PyQt4.QtGui import QLabel, QLineEdit, QTimeEdit, QComboBox, QPushButton, QCheckBox, QPlainTextEdit
from test.cute.widgets import LabelDriver, LineEditDriver, DateTimeEditDriver, ComboBoxDriver, ButtonDriver, \
    TextEditDriver, WidgetDriver


class BaseDriver(WidgetDriver):
    def label(self, matching):
        return LabelDriver.findSingle(self, QLabel, matching)

    def lineEdit(self, matching):
        return LineEditDriver.findSingle(self, QLineEdit, matching)

    def textEdit(self, matching):
        return TextEditDriver.findSingle(self, QPlainTextEdit, matching)

    def dateTimeEdit(self, matching):
        return DateTimeEditDriver.findSingle(self, QTimeEdit, matching)

    def combobox(self, matching):
        return ComboBoxDriver.findSingle(self, QComboBox, matching)

    def button(self, matching):
        return ButtonDriver.findSingle(self, QPushButton, matching)

    def checkbox(self, matching):
        return ButtonDriver.findSingle(self, QCheckBox, matching)