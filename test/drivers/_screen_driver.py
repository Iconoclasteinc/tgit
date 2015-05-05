from PyQt5.QtWidgets import QLabel, QLineEdit, QTimeEdit, QComboBox, QPushButton, QCheckBox, QPlainTextEdit, \
    QTableView, QWidget, QTextEdit, QRadioButton

from cute.widgets import LabelDriver, LineEditDriver, DateTimeEditDriver, ComboBoxDriver, ButtonDriver, \
    TextEditDriver, WidgetDriver, TableViewDriver


class ScreenDriver(WidgetDriver):
    def label(self, matching):
        return LabelDriver.find_single(self, QLabel, matching)

    def lineEdit(self, matching):
        return LineEditDriver.find_single(self, QLineEdit, matching)

    def textEdit(self, matching):
        return TextEditDriver.find_single(self, QPlainTextEdit, matching)

    def rich_text_edit(self, *matching):
        return TextEditDriver.find_single(self, QTextEdit, *matching)

    def dateTimeEdit(self, matching):
        return DateTimeEditDriver.find_single(self, QTimeEdit, matching)

    def combobox(self, matching):
        return ComboBoxDriver.find_single(self, QComboBox, matching)

    def button(self, matching):
        return ButtonDriver.find_single(self, QPushButton, matching)

    def checkbox(self, matching):
        return ButtonDriver.find_single(self, QCheckBox, matching)

    def radio(self, matching):
        return ButtonDriver.find_single(self, QRadioButton, matching)

    def table(self, matching):
        return TableViewDriver.find_single(self, QTableView, matching)

    def widget(self, matching):
        return WidgetDriver.find_single(self, QWidget, matching)