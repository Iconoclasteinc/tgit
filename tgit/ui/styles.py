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

Main = """
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
    }

    WelcomeScreen #welcome-dialog QPushButton:hover {
        background-color: #D42023;
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

    #navigation, #buttons {
        background-color: #595959;
    }

    QToolButton#add {
        background-color: #EC2327;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        color: white;
        padding: 12px 12px 9px;
    }

    QToolButton#add:hover {
        background-color: #D42023;
    }

    QPushButton#next {
        padding: 2px;
        padding-right: 12px;
        color: #F25C0A;
        background-color: transparent;
        border-image: url(:/next.png) 1 12 1 1;
        border-top: 1px transparent;
        border-bottom: 1px transparent;
        border-right: 12px transparent;
        border-left: 12px transparent;
    }

    QPushButton#next:disabled {
        border-image: none;
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
"""

