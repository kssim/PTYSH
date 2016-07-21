
class _Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(_Singleton('Singleton', (object,), {})): pass

class Parser(Singleton):

    def __init__(self):
        return

    def command_parser(self, command):
        print command
        return
