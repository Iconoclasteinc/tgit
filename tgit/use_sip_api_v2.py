# -*- coding: utf-8 -*-

import sip

# Use Sip API v2
for name in ("QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant"):
    sip.setapi(name, 2)