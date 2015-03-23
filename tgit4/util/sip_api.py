# -*- coding: utf-8 -*-

import sip


def use_v2():
    for name in ("QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant"):
        sip.setapi(name, 2)