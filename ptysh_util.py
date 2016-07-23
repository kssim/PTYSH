import signal
import hashlib

class _Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(_Singleton('Singleton', (object,), {})): pass


class Signal(Singleton):

    def empty_signal_handler(self, in_signal, in_frame):
        return

    def set_signal(self):
        signal.signal(signal.SIGINT, self.empty_signal_handler)
        signal.signal(signal.SIGTSTP, self.empty_signal_handler)


class Encryption(object):

    _salt = 'IPOT_PTYSH'
    _default_passwd = '5b92b30b5d3e1a6f0dbe1824f4b7b1414bab66396ff0af3b2a329b40c8926146'    # ptysh

    def encrypt_passwd(self, in_passwd):
        return hashlib.sha256(self._salt.encode() + in_passwd.encode()).hexdigest()

    def validate_passwd(self, in_passwd):
        return True if self._default_passwd == self.encrypt_passwd(in_passwd) else False


class Login(Singleton):

    _login_state = False

    def get_login_state(self):
        return self._login_state

    def set_login_state(self, in_state):
        self._login_state = in_state
