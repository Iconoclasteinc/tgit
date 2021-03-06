from PyQt5.QtWidgets import QLabel, QLineEdit, QTimeEdit, QComboBox, QCheckBox, QPlainTextEdit, \
    QTableView, QTextEdit, QRadioButton, QDateEdit, QToolButton, QTabWidget, QAbstractButton, QListWidget

from cute.widgets import LabelDriver, LineEditDriver, QDateTimeEditDriver, ComboBoxDriver, ButtonDriver, \
    TextEditDriver, WidgetDriver, TableViewDriver, QToolButtonDriver, QTabWidgetDriver, QListViewDriver


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
        return QDateTimeEditDriver.find_single(self, QTimeEdit, matching)

    def dateEdit(self, matching):
        return QDateTimeEditDriver.find_single(self, QDateEdit, matching)

    def combobox(self, matching):
        return ComboBoxDriver.find_single(self, QComboBox, matching)

    def button(self, matching):
        return ButtonDriver.find_single(self, QAbstractButton, matching)

    def tool_button(self, matching):
        return QToolButtonDriver.find_single(self, QToolButton, matching)

    def checkbox(self, matching):
        return ButtonDriver.find_single(self, QCheckBox, matching)

    def radio(self, matching):
        return ButtonDriver.find_single(self, QRadioButton, matching)

    def table(self, matching):
        return TableViewDriver.find_single(self, QTableView, matching)

    def tabs(self, matching):
        return QTabWidgetDriver.find_single(self, QTabWidget, matching)

    def list_view(self, matching):
        return QListViewDriver.find_single(self, QListWidget, matching)
