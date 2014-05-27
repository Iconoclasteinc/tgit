# -*- coding: utf-8 -*-
#
# TGiT, Music Tagger for Professionals
# Copyright (C) 2013 Iconoclaste Musique Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QLabel, QFormLayout, QLineEdit, QSizePolicy, QComboBox, QTimeEdit, QPushButton, QCheckBox, \
    QHBoxLayout, QVBoxLayout
from tgit.ui.widgets.text_area import TextArea


def layout():
    form = QFormLayout()
    form.setContentsMargins(0, 0, 0, 0)
    form.setLabelAlignment(Qt.AlignVCenter)
    form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
    return form


def column():
    column = QVBoxLayout()
    column.setContentsMargins(0, 0, 0, 0)
    return column


def row():
    row = QHBoxLayout()
    row.setContentsMargins(0, 0, 0, 0)
    return row


def labelFor(field, title):
    label = QLabel(title)
    label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    label.setBuddy(field)
    return label


def label(name=None):
    label = QLabel()
    label.setObjectName(name)
    return label


def lineEdit(name):
    edit = QLineEdit()
    edit.setObjectName(name)
    return edit


def textArea(name):
    text = TextArea()
    text.setObjectName(name)
    sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    sizePolicy.setVerticalStretch(1)
    text.setSizePolicy(sizePolicy)
    text.setTabChangesFocus(True)
    return text


def comboBox(name):
    combo = QComboBox()
    combo.setObjectName(name)
    combo.setEditable(True)
    combo.setInsertPolicy(QComboBox.NoInsert)
    combo.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
    return combo


def timeEdit(name):
    time = QTimeEdit()
    time.setObjectName(name)
    time.setDisplayFormat('mm:ss')
    return time


def button(name):
    button = QPushButton()
    button.setObjectName(name)
    button.setFocusPolicy(Qt.StrongFocus)
    button.setCursor(Qt.PointingHandCursor)
    return button


def checkBox(name):
    checkbox = QCheckBox()
    checkbox.setObjectName(name)
    checkbox.setFocusPolicy(Qt.StrongFocus)
    return checkbox


def enableButton(button):
    button.setEnabled(True)
    button.setCursor(Qt.PointingHandCursor)


def disableButton(button):
    button.setDisabled(True)
    button.setCursor(Qt.ArrowCursor)