#!/usr/bin/env python

import tgit

from PyQt4.QtCore import QSysInfo
from PyQt4.QtGui import QFont

if hasattr(QSysInfo, 'MacintoshVersion') and QSysInfo.MacintoshVersion > QSysInfo.MV_10_8:
    # fix Mac OS X 10.9 (mavericks) font issue on Qt 4.8.5
    # https://bugreports.qt-project.org/browse/QTBUG-32789
    QFont.insertSubstitution(".Lucida Grande UI", "Lucida Grande")


import tgit.app

tgit.app.main()