# -*- coding: utf-8 -*-

import sip

API_NAMES = ("QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant")
VERSION_2 = 2

for name in API_NAMES:
    sip.setapi(name, VERSION_2)