import signal

class _Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(_Singleton('Singleton', (object,), {})): pass


class Signal(Singleton):

    def empty_signal_handler(self, signal, frame):
        return

    def set_signal(self):
        signal.signal(signal.SIGINT, self.empty_signal_handler)
        signal.signal(signal.SIGTSTP, self.empty_signal_handler)
