import sys
import signal
from os import path
from hashlib import sha256

HOST_NAME_FILE_PATH = '/etc/hostname'

class _Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(_Singleton('Singleton', (object,), {})): pass


class IoControl(object):

    def __init__(self):
        self._host_name = self.get_host_name()

    def get_input_command(self):
        prompt_msg = self.get_prompt_msg()
        return input(prompt_msg) if sys.version_info >= (3,0) else raw_input(prompt_msg)

    def get_host_name(self):
        if path.exists(HOST_NAME_FILE_PATH) == False:
            return "PTYSH"          # default prompt name

        with open(HOST_NAME_FILE_PATH, "rb") as f:
            return f.readline().strip()

    def get_prompt_msg(self):
        prompt = "#" if Status().login else ">"

        if Status().module_depth > Status().ZERO_DEPTH:
            location = "(%s)" % Status().current_node
        else:
            location = ""

        formatted_prompt = "%s%s%s " % (self._host_name.decode('utf-8'), location, prompt)
        return formatted_prompt

    def print_hello_message(self):
        message = "Hello, This is Python Teletype Shell.\n"
        message += "COPYRIGHT 2017 KyeongSeob Sim. ALL RIGHTS RESERVED.\n"
        self.print_msg(message)

    def print_list(self, command, description):
        self.print_msg("  %s%s" % (command.ljust(30), description))

    def print_msg(self, msg):
        print (msg)

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

    ZERO_DEPTH = 0
    CONF_DEPTH = 1

    def __init__(self):
        self._login = False
        self._module_depth = self.ZERO_DEPTH
        self._current_node = []

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, state):
        self._login = state

    @property
    def module_depth(self):
        return self._module_depth

    def increase_module_depth(self):
        self._module_depth += 1

    def decrease_module_depth(self):
        self._module_depth -= 1

    @property
    def current_node(self):
        return "" if len(self._current_node) == 0 else self._current_node[-1]

    def push_current_node(self, node_name):
        self._current_node.append(node_name)

    def pop_current_node(self):
        self._current_node.pop()


class LoadModule(object):

    def __init__(self, module_path):
        self.module_path = module_path
        self.module_name = self.get_module_name()

    def get_module_name(self):
        """
        Get the name of the module to load.
        Except that the extension is not "py" and the filename is "__init__".
        """
        file_name, file_extension = path.splitext(self.module_path)
        if file_extension != ".py" or file_name == "__init__":
            return ""

        return file_name

    def get_instance(self):
        """
        Load the module.
        If the module name does not exist or an exception is thrown, it returns None.
        """
        if self.module_name == "":
            return None

        try:
            module = __import__(self.module_name)
            self.instance = getattr(module, self.module_name, None)
        except Exception as e:
            io = IoControl()
            io.print_msg("Module \"%s\" has something problem." % self.module_name)
            io.print_msg(e)
            return None

        return self.instance()
