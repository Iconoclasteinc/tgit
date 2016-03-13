def Closeable(cls):
    """Decorator for closeable widgets. Closeable widgets emit a closed signal on close.
    :param cls: The decorated class
    """
    widget_close = cls.close

    def close(self):
        is_closed = widget_close(self)
        if is_closed:
            self.closed.emit()
        return is_closed

    cls.close = close

    return cls
