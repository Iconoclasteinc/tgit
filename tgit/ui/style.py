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
from PyQt4 import QtGui

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QHBoxLayout, QVBoxLayout, QFormLayout, QColor, QFrame


# Using stylesheets on the table corrupts the display of the button widgets in the
# cells, at least on OSX. So we have to style programmatically
TABLE_COLUMNS_WIDTHS = [345, 205, 215, 85, 65, 30, 30]
TABLE_BACKGROUND_COLOR = Qt.white
TABLE_BORDER_COLOR = QColor.fromRgb(0xDDDDDD)
TABLE_BORDER_STYLE = QFrame.Panel | QFrame.Plain


def enableButton(button):
    button.setEnabled(True)
    button.setCursor(Qt.PointingHandCursor)


def disableButton(button):
    button.setDisabled(True)
    button.setCursor(Qt.ArrowCursor)


def resetMargins(layout):
    layout.setContentsMargins(0, 0, 0, 0)
    return layout


def horizontalLayout():
    return resetMargins(QHBoxLayout())


def verticalLayout():
    return resetMargins(QVBoxLayout())


def formLayout():
    layout = resetMargins(QFormLayout())
    layout.setLabelAlignment(Qt.AlignVCenter)
    layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
    return layout


Sheet = """
    MainWindow {
        background-color: #F6F6F6;
        margin: 0;
        padding: 0;
    }

    #welcome-screen {
        background-color: rgba(0, 0, 0, 70%);
    }

    #welcome-screen #welcome-dialog {
        padding: 20px;
        min-width: 500px;
        max-width: 500px;
        min-height: 300px;
        max-height: 300px;
        background: white url(':/logo.png') no-repeat top left;
    }

    #welcome-screen #welcome-dialog #logo {
        min-width: 58;
        min-height: 105;
    }

    #welcome-screen #welcome-dialog QPushButton {
        background-color: #EC2327;
        border: 2px solid #EC2327;
        border-radius: 4px;
        font-size: 16px;
        font-weight: bold;
        color: white;
        padding: 14px 14px 11px 14px;
    }

    #welcome-screen #welcome-dialog QPushButton:hover {
        background-color: #D42023;
        border-color: #D42023;
    }

    #welcome-screen #welcome-dialog QPushButton:pressed {
        border: 2px solid white;
    }

    #welcome-screen #welcome-dialog QLabel[title='h1'] {
        font-size: 28px;
        font-weight: bold;
        margin-top: 35px;
        margin-bottom: 50px;
    }

    #welcome-screen #welcome-dialog QLabel {
        color: #2D2D25;
        font-size: 16px;
    }

    QStackedWidget {
        margin: 0 15px 15px 15px;
    }

    #navigation {
        min-height: 48px;
    }

    #controls {
        min-height: 64px;
    }

    QToolButton#add-tracks {
        background-color: #EC2327;
        border: 2px solid #EC2327;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        color: white;
        padding: 10px 10px 7px 10px;
    }

    QToolButton#add-tracks:hover {
        background-color: #D42023;
        border-color: #D42023;
    }

    QToolButton#add-tracks:pressed {
        border: 2px solid #F6F6F6;
    }

    #navigation, #controls {
        background-color: #595959;
    }

    #controls QPushButton#previous {
        padding: 4px 2px 2px 12px;
        color: white;
        background-color: transparent;
        border-image: url(:/previous.png) 1 1 1 12;
        border-top: 1px transparent;
        border-right: 12px transparent;
        border-bottom: 1px transparent;
        border-left: 12px transparent;
        margin-left: 14px;
        text-align: left;
    }

    #controls QPushButton#previous:disabled {
        border-image: url(:/nothing.png) 1 1 1 1;
        background-color: transparent;
        color: transparent;
    }

    #controls QPushButton#save {
        border: 2px solid #F25C0A;
        border-radius: 5px;
        background-color: #F25C0A;
        font-size: 15px;
        min-width: 150px;
        min-height: 15px;
        font-weight: bold;
        color: white;
        padding: 13px 13px 10px 13px;
    }

    #controls QPushButton#save:disabled {
        background-color: transparent;
        border: none;
        color: transparent;
    }

    #controls QPushButton#save:focus, #controls QPushButton#save:hover {
        background-color: #D95109;
        border-color: #D95109;
    }

    #controls QPushButton#save:pressed {
        border: 2px solid #595959;
    }

    #controls QPushButton#next {
        padding: 4px 12px 2px 2px;
        color: #F25C0A;
        background-color: transparent;
        border-image: url(:/next.png) 1 12 1 1;
        border-top: 1px transparent;
        border-right: 12px transparent;
        border-bottom: 1px transparent;
        border-left: 12px transparent;
        margin-right: 14px;
        text-align: right;
    }

    #controls QPushButton#next:disabled {
        border-image: url(:/nothing.png) 1 1 1 1;
        background-color: transparent;
        color: transparent;
    }

    QTableView QHeaderView {
        background-color: white;
    }

    QTableView QTableCornerButton::section:vertical {
        background-color: white;
        border-top: 1px solid #F7C3B7;
        border-bottom: 1px solid #F7C3B7;
        border-right: 1px solid  #F2F2F2;
    }

    QTableView QHeaderView::section {
        background: transparent;
        border: 0;
    }

    QTableView QHeaderView::section:horizontal {
        text-align: left;
        font-weight: bold;
        font-size: 13px;
        padding: 21px 0 18px 5px;
        border-top: 1px solid #F7C3B7;
        border-bottom: 1px solid #F7C3B7;
        border-right: 1px solid  #F2F2F2;
        min-height: 15px;
    }

    QTableView QHeaderView::section:vertical {
        padding: 4px 7px 0px;
        border-bottom: 1px solid #F7C3B7;
        border-right: 1px solid #F7C3B7;
    }

    QTableView::item {
        border-bottom: 1px solid #F7C3B7;
    }

    QTableView::item:alternate {
        background-color: #F9F7F7;
    }

    QToolButton#play-track {
        border-image: url(:/play.png);
    }

    QToolButton#play-track:hover {
        border-image: url(:/play-hover.png);
    }

    QToolButton#play-track:pressed {
        border-image: url(:/play-pressed.png);
    }

    QToolButton#play-track:checked {
        border-image: url(:/stop.png);
    }

    QToolButton#play-track:checked:hover {
        border-image: url(:/stop-hover.png);
    }

    QToolButton#play-track:checked:pressed {
        border-image: url(:/stop-pressed.png);
    }

    QToolButton#remove-track {
        border-image: url(:/remove.png);
    }

    QToolButton#remove-track:hover {
        border-image: url(:/remove-hover.png);
    }

    QToolButton#remove-track-track:pressed {
        border-image: url(:/remove-pressed.png);
    }

    #album-edition-page QGroupBox, #track-edition-page QGroupBox {
        border: 1px solid #DDDDDD;
        border-bottom: 2px solid rgba(0, 0, 0, 20%);
        background-color: white;
        padding: 17px 14px 14px 0px;
        margin: 5px 8px;
        font-size: 10px;
    }

    #album-edition-page QGroupBox::title, #track-edition-page QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 1px;
        padding: 0 3px;
        color: #777777;
        border: 1px solid #DFDFDF;
        background-color: #F7F7F7;
     }

    #album-edition-page QGroupBox#pictures {
        padding: 13px 14px 10px 14px;
     }

    #album-edition-page QGroupBox#pictures::title {
        background-color: transparent;
        color: transparent;
        border: none;
     }

    #album-edition-page QGroupBox#pictures #front-cover {
        min-width: 350px;
        max-width: 350px;
        min-height: 350px;
        max-height: 350px;
        background-color: #F9F9F9;
        border: 1px solid #F79D6C;
    }

    #album-edition-page QPushButton#select-picture {
        background-image: url(:/add-picture.png);
        background-repeat: no-repeat;
        background-position: left center;
        background-origin: border;
        background-color: #F25C0A;
        border: 2px solid #F25C0A;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        color: white;
        padding: 10px 10px 7px 34px;
    }

    #album-edition-page QPushButton#remove-picture {
        background-color: #F25C0A;
        border: 2px solid #F25C0A;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        color: white;
        padding: 10px 10px 7px 10px;
        margin-left: 10px;
    }

    #album-edition-page QPushButton#select-picture:hover,
    #album-edition-page QPushButton#select-picture:focus,
    #album-edition-page QPushButton#remove-picture:hover,
    #album-edition-page QPushButton#remove-picture:focus {
        background-color: #D95109;
        border-color: #D95109;
    }

    #album-edition-page QPushButton#select-picture:pressed,
    #album-edition-page QPushButton#remove-picture:pressed {
        border: 2px solid white;
    }

    #album-edition-page QLineEdit, #album-edition-page TextArea, #album-edition-page QComboBox,
    #album-edition-page QComboBox::drop-down, #album-edition-page QComboBox QAbstractItemView,
    #track-edition-page QLineEdit, #track-edition-page TextArea, #track-edition-page QComboBox,
    #track-edition-page QComboBox::drop-down, #track-edition-page QComboBox QAbstractItemView {
        background-color: #F9F9F9;
        border: 1px solid #B1B1B1;
        color: #222222;
        min-height: 20px;
    }

    #album-edition-page QLineEdit:focus, #album-edition-page TextArea:focus, #album-edition-page QComboBox:focus,
    #album-edition-page QComboBox:on, #album-edition-page QComboBox::drop-down:focus,
    #album-edition-page QComboBox::drop-down:on, #album-edition-page QComboBox QAbstractItemView:focus,
    #track-edition-page QLineEdit:focus, #track-edition-page TextArea:focus, #track-edition-page QComboBox:focus,
    #track-edition-page QComboBox:on, #track-edition-page QComboBox::drop-down:focus,
    #track-edition-page QComboBox::drop-down:on, #track-edition-page QComboBox QAbstractItemView:focus  {
        border: 1px solid #F79D6C;
    }

    #album-edition-page QLineEdit:disabled, #album-edition-page TextArea:disabled,
    #track-edition-page QLineEdit:disabled, #track-edition-page TextArea:disabled {
        background-color: #FCFCFC;
        border-color: #E7E7E7;
    }

    #album-edition-page QCheckBox {
        min-height: 20px;
        padding: 1px 2px 2px 2px;
    }

    QCheckBox::indicator {
        width: 14px;
        height: 14px;
        subcontrol-position: left center;
    }

    QCheckBox::indicator:unchecked {
        image: url(:/checkbox.png);
    }

    QCheckBox::indicator:unchecked:hover, QCheckBox::indicator:unchecked:focus {
        image: url(:/checkbox-hover.png);
    }

    QCheckBox::indicator:unchecked:pressed {
        image: url(:/checkbox-pressed.png);
    }

    QCheckBox::indicator:checked {
        image: url(:/checkbox-checked.png);
    }

    QCheckBox::indicator:checked:hover, QCheckBox::indicator:checked:focus {
        image: url(:/checkbox-checked-hover.png);
    }

    QCheckBox::indicator:checked:pressed {
        image: url(:/checkbox-checked-pressed.png);
    }

    #album-edition-page #comments {
        max-height: 3.5em;
    }

    #album-edition-page QLabel, #track-edition-page QLabel {
        color: #444444;
        min-width: 175px;
    }

    #track-edition-page #content QLabel {
        min-width: 125px;
    }

    #album-edition-page QLabel:disabled, #track-edition-page QLabel:disabled {
        color: #C2C2C2;
    }

    #album-edition-page QComboBox::drop-down, #track-edition-page QComboBox::drop-down {
        padding: 0;
        margin: 0;
        subcontrol-origin: border;
        subcontrol-position: top right;
        width: 20px;
    }

    QComboBox::down-arrow {
        image: url(:/down-arrow.png);
    }

    QComboBox::down-arrow:on, QComboBox::down-arrow:focus {
        image: url(:/down-arrow-on.png);
    }

    #album-banner {
        background-color: white;
        border: 1px solid #DDDDDD;
        border-bottom: 2px solid rgba(0, 0, 0, 20%);
        margin: 0px 8px;
        padding: 14px;
        max-height: 50px;
    }

    #album-banner #album-cover {
        min-width: 50px;
        max-width: 50px;
        min-height: 50px;
        max-height: 50px;
        background-color: #F9F9F9;
        border: 1px solid #B8B8B8;
        margin-right: 15px;
    }

    #album-banner QLabel {
        color: #777777;
        padding: 0;
        margin: 0;
        min-width: 0;
    }

    #album-banner QLabel[title='h2'] {
        font-size: 22px;
    }

    #album-banner QLabel[title='h3'] {
        font-size: 14px;
    }

    #track-edition-page #software-notice {
        font-size: 10px;
        margin-right: 8px;
    }
 """

MAC = hasattr(QtGui, "qt_mac_set_native_menubar")

if MAC:
    Sheet += """
        #album-edition-page QComboBox, #track-edition-page QComboBox {
            padding-left: 1px;
            padding-top: 1px;
            margin-left: 3px;
            margin-right: 2px;
        }
    """

    #album-edition-page QComboBox QAbstractItemView QScrollBar {
    #     padding: 0;
    #     margin: 0;
    #     background: transparent;
    #     width: 20px;
    # }
