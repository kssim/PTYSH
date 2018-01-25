# -*- coding: utf-8 -*-

"""
"""

import signal
from os import path
from hashlib import sha256

from inout import IoControl
from structure import Singleton

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
