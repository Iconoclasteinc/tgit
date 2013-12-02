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
from PyQt4.QtGui import QHBoxLayout, QVBoxLayout, QFormLayout


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

    WelcomeScreen {
        background-color: rgba(0, 0, 0, 70%);
    }

    WelcomeScreen #welcome-dialog {
        padding: 20px;
        min-width: 500px;
        max-width: 500px;
        min-height: 300px;
        max-height: 300px;
        background: white url(':/logo.png') no-repeat top left;
    }

    WelcomeScreen #welcome-dialog #logo {
        min-width: 58;
        min-height: 105;
    }

    WelcomeScreen #welcome-dialog QPushButton {
        background-color: #EC2327;
        border-radius: 4px;
        font-size: 16px;
        font-weight: bold;
        color: white;
        padding: 16px 16px 13px;
        min-width: 150px;
    }

    WelcomeScreen #welcome-dialog QPushButton:hover {
        background-color: #D42023;
    }

    WelcomeScreen #welcome-dialog QPushButton:pressed {
        border: 2px solid rgba(0, 0, 0, 30%);
    }

    WelcomeScreen #welcome-dialog QLabel[title='h1'] {
        font-size: 28px;
        font-weight: bold;
        margin-top: 35px;
        margin-bottom: 50px;
    }

    WelcomeScreen #welcome-dialog QLabel {
        color: #2D2D25;
        font-size: 16px;
    }

    QStackedWidget {
        margin: 15px;
    }

    #navigation {
        min-height: 48px;
    }

    #buttons {
        min-height: 64px;
    }

    QToolButton#add {
        background-color: #EC2327;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        color: white;
        padding: 12px 12px 9px;
        min-width: 100px;
    }

    QToolButton#add:hover {
        background-color: #D42023;
    }

    QToolButton#add:pressed {
        border: 2px solid rgba(0, 0, 0, 30%);
    }

    #navigation, #buttons {
        background-color: #595959;
    }

    #buttons QPushButton#previous {
        padding: 2px;
        padding-left: 12px;
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

    #buttons QPushButton#previous:disabled {
        border-image: url(:/nothing.png) 1 1 1 1;
        background-color: transparent;
        color: transparent;
    }

    #buttons QPushButton#save {
        border-radius: 5px;
        background-color: #F25C0A;
        font-size: 15px;
        font-weight: bold;
        color: white;
        padding: 12px 12px 9px;
        min-width: 150px;
    }

    #buttons QPushButton#save:pressed {
        border: 2px solid rgba(0, 0, 0, 30%);
    }

    #buttons QPushButton#save:disabled {
        background-color: transparent;
        color: transparent;
    }

    #buttons QPushButton#save:focus, #buttons QPushButton#save:hover  {
        background-color: #D95109;
    }

    #buttons QPushButton#next {
        padding: 2px;
        padding-right: 12px;
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

    #buttons QPushButton#next:disabled {
        border-image: url(:/nothing.png) 1 1 1 1;
        background-color: transparent;
        color: transparent;
    }

    QTableView {
        border: 1px solid #DDDDDD;
        border-bottom: 2px solid rgba(0, 0, 0, 20%);
        background-color: white;
        padding: 10px;
        qproperty-alternatingRowColors: true;
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

    QToolButton#play {
        border-image: url(:/play.png);
    }

    QToolButton#play:hover {
        border-image: url(:/play-hover.png);
    }

    QToolButton#play:pressed {
        border-image: url(:/play-pressed.png);
    }

    QToolButton#play:checked {
        border-image: url(:/stop.png);
    }

    QToolButton#play:checked:hover {
        border-image: url(:/stop-hover.png);
    }

    QToolButton#play:checked:pressed {
        border-image: url(:/stop-pressed.png);
    }

    QToolButton#remove {
        border-image: url(:/remove.png);
    }

    QToolButton#remove:hover {
        border-image: url(:/remove-hover.png);
    }

    QToolButton#remove:pressed {
        border-image: url(:/remove-pressed.png);
    }

    #album-page QGroupBox {
        border: 1px solid #DDDDDD;
        border-bottom: 2px solid rgba(0, 0, 0, 20%);
        background-color: white;
        padding: 17px 14px 10px 0px;
        margin: 5px 8px;
        font-size: 10px;
    }

    #album-page QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 1px;
        padding: 0 3px;
        color: #777777;
        border: 1px solid #DFDFDF;
        background-color: #F7F7F7;
     }

    #album-page QGroupBox#pictures {
        padding: 13px 14px 10px 14px;
     }

    #album-page QGroupBox#pictures::title {
        background-color: transparent;
        color: transparent;
        border: none;
     }

    #album-page QGroupBox#pictures #front-cover {
        min-width: 350px;
        max-width: 350px;
        min-height: 350px;
        max-height: 350px;
        background-color: #F9F9F9;
        border: 1px solid #F79D6C;
    }

    #album-page QPushButton#select-picture {
        background-image: url(:/add-picture.png);
        background-repeat: no-repeat;
        background-position: left center;
        background-origin: border;
        background-color: #F25C0A;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        color: white;
        padding: 12px 12px 9px 37px;
        min-width: 125px;
    }

    #album-page QPushButton#select-picture:hover, #album-page QPushButton#select-picture:focus {
        background-color: #D95109;
    }

    #album-page QPushButton#select-picture:pressed {
        border: 2px solid rgba(0, 0, 0, 30%);
    }


    #album-page QLineEdit, #album-page TextArea {
        background-color: #F9F9F9;
        border: 1px solid #B1B1B1;
        color: #222222;
        min-height: 20px;
    }

    #album-page QLineEdit:focus, #album-page TextArea:focus {
        border: 1px solid #F79D6C;
        selection-background-color: qlineargradient(x1:0, y1:0, x2:0, y2: 1, stop:0 #FFB200 stop:1 #FFA200);
    }

    #album-page QLineEdit:disabled, #album-page TextArea:disabled {
        background-color: #FCFCFC;
        border-color: #E7E7E7;
    }

    #album-page #comments {
        max-height: 3.5em;
    }

    #album-page QLabel {
        color: #444444;
        min-width: 175px;
    }

    #album-page QLabel:disabled {
        color: #C2C2C2;
    }
"""

