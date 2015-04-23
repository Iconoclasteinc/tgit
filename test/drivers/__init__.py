# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel, QLineEdit, QTimeEdit, QComboBox, QPushButton, QCheckBox, QPlainTextEdit, \
    QTableView, QWidget, QTextEdit

from test.cute.widgets import LabelDriver, LineEditDriver, DateTimeEditDriver, ComboBoxDriver, ButtonDriver, \
    TextEditDriver, WidgetDriver, TableViewDriver


class BaseDriver(WidgetDriver):
    def label(self, matching):
        return LabelDriver.findSingle(self, QLabel, matching)

    def lineEdit(self, matching):
        return LineEditDriver.findSingle(self, QLineEdit, matching)

    def textEdit(self, matching):
        return TextEditDriver.findSingle(self, QPlainTextEdit, matching)

    def rich_text_edit(self, *matching):
        return TextEditDriver.findSingle(self, QTextEdit, *matching)

    def dateTimeEdit(self, matching):
        return DateTimeEditDriver.findSingle(self, QTimeEdit, matching)

    def combobox(self, matching):
        return ComboBoxDriver.findSingle(self, QComboBox, matching)

    def button(self, matching):
        return ButtonDriver.findSingle(self, QPushButton, matching)

    def checkbox(self, matching):
        return ButtonDriver.findSingle(self, QCheckBox, matching)

    def table(self, matching):
        return TableViewDriver.findSingle(self, QTableView, matching)

    def widget(self, matching):
        return WidgetDriver.findSingle(self, QWidget, matching)