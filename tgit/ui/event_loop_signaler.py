from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal


def in_event_loop(slot):
    return EventLoopSignaler(slot)


class EventLoopSignaler(QObject):
    fire = pyqtSignal(tuple)

    def __init__(self, slot):
        super().__init__()
        self.fire.connect(lambda args: slot(*args))

    def __call__(self, *args):
        self.fire.emit(args)
