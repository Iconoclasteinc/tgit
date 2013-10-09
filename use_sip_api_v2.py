# -*- coding: utf-8 -*-

import sip

API_NAMES = ("QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant")
VERSION_2 = 2


def useVersion(version):
    for name in API_NAMES:
        sip.setapi(name, version)

useVersion(VERSION_2)