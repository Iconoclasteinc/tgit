from cute import event_loop, platforms

PAUSE_AFTER_DISPLAY = 25 if platforms.linux else 0
# todo see if we can replace the end of test pause with this one on Linux
PAUSE_AFTER_CLOSE = 0


def show_(widget, pause=PAUSE_AFTER_DISPLAY):
    widget.show()
    event_loop.process_events_for(pause)


def close_(driver, pause=PAUSE_AFTER_CLOSE):
    driver.close()
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
