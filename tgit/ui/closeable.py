# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal, QObject


def Closeable(cls):
    """Decorator for closeable widgets. Closeable widgets emit a closed signal on close."""
    widget_close = cls.close

    def on_close(self, do):
        self.closed.connect(do)

    def close(self):
        is_closed = widget_close(self)
        if is_closed:
            self.closed.emit()
        return is_closed

    cls.on_close = on_close
    cls.close = close

    return cls
