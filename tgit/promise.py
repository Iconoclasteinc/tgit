from concurrent.futures import Future


class Promise:
    def __init__(self, future=None):
        self._future = future if future is not None else Future()

    def on_complete(self, do):
        def done(f):
            if f.cancelled():
                return
            if f.exception() is None:
                do(f.result(), None)
            else:
                do(None, f.exception())

        self._future.add_done_callback(done)

    def on_success(self, do):
        self.on_complete(lambda result, error: do(result) if result is not None else None)

    def on_failure(self, do):
        self.on_complete(lambda result, error: do(error) if error is not None else None)

    # I just had to add that parameter
    def result(self, wait_for_secs=None):
        return self._future.result(wait_for_secs)

    def complete(self, result):
        self._future.set_result(result)

    def error(self, error):
        self._future.set_exception(error)