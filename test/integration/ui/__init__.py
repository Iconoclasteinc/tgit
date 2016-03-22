from cute import event_loop, platforms

PAUSE_AFTER_DISPLAY = 25 if platforms.linux else 0


def show_(widget, pause=PAUSE_AFTER_DISPLAY):
    widget.adjustSize()
    widget.show()
    event_loop.process_events_for(pause)


# noinspection PyUnusedLocal
def ignore(*args, **kwargs):
    pass


def raise_(e):
    raise e


def no(*_):
    return False


def yes(*_):
    return True
