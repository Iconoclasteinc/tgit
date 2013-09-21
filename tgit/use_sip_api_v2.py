import sip

API_VERSION = 2
API_NAMES = ("QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant")

for name in API_NAMES:
    sip.setapi(name, API_VERSION)