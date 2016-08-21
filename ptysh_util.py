import signal
import sys
from hashlib import sha256
from os import path

HOST_NAME_FILE_PATH = '/etc/hostname'

class _Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(_Singleton('Singleton', (object,), {})): pass


class IoControl(object):

    _host_name = ''

    def __init__(self):
        self._host_name = self.get_host_name()

    def get_input_command(self):
        return input() if sys.version_info >= (3,0) else raw_input()

    def set_prompt(self):
        prompt = '#' if Status().login_state == True else '>'

        if Status().sub_node == True:
            location = '(%s)' % Status().current_node
        elif Status().configure_terminal_state == True:
            location = '(configure terminal)'
        else:
            location = ''

        formatted_prompt = '%s%s%s ' % (self._host_name.decode('utf-8'), location, prompt)
        sys.stdout.write(formatted_prompt)

    def print_hello_message(self):
        message = 'Hello, This is Python Teletype Shell.\n'
        message += 'COPYRIGHT 2016 IPOT. ALL RIGHTS RESERVED.\n\n'
        sys.stdout.write(message)

    def get_host_name(self):
        if path.exists(HOST_NAME_FILE_PATH) == False:
            return 'PTYSH'          # default prompt name

        with open(HOST_NAME_FILE_PATH, 'rb') as f:
            return f.readline().strip()


class Signal(Singleton):

    def empty_signal_handler(self, in_signal, in_frame):
        return

    def set_signal(self):
        signal.signal(signal.SIGINT, self.empty_signal_handler)
        signal.signal(signal.SIGTSTP, self.empty_signal_handler)


class Encryption(object):

    _salt = 'IPOT_PTYSH'
    _default_passwd = '5b92b30b5d3e1a6f0dbe1824f4b7b1414bab66396ff0af3b2a329b40c8926146'    # Encrypted string 'ptysh'

    def encrypt_passwd(self, in_passwd):
        return sha256(self._salt.encode() + in_passwd.encode()).hexdigest()

    def validate_passwd(self, in_passwd):
        return True if self._default_passwd == self.encrypt_passwd(in_passwd) else False


class Status(Singleton):

    _login_state = False
    _configure_terminal_state = False
    _sub_node = False
    _current_node = ''

    @property
    def login_state(self):
        return self._login_state

    @login_state.setter
    def login_state(self, in_state):
        self._login_state = in_state

    @property
    def configure_terminal_state(self):
        return self._configure_terminal_state

    @configure_terminal_state.setter
    def configure_terminal_state(self, in_state):
        self._configure_terminal_state = in_state

    @property
    def sub_node(self):
        return self._sub_node

    @sub_node.setter
    def sub_node(self, in_state):
        if in_state == False:
            self._current_node = ''

        self._sub_node = in_state

    @property
    def current_node(self):
        return self._current_node

    @current_node.setter
    def current_node(self, in_node_name):
        self._current_node = in_node_name


class LoadModule(object):

    _instance = None

    def __init__(self, in_module_name, in_class_name):
        module = __import__(in_module_name)
        self._instance = getattr(module, in_class_name)

    @property
    def instance(self):
        return self._instance()
