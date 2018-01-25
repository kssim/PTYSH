# -*- coding: utf-8 -*-

"""
Modules that define utilities used by PTYSH.
"""

import signal
from os import path
from hashlib import sha256

from inout import IoControl
from structure import Singleton

class Signal(Singleton):

    """
    Classes for handling various signals.
    """

    def empty_signal_handler(self, signal, frame):
        return

    def init_signal(self):
        signal.signal(signal.SIGINT, self.empty_signal_handler)
        signal.signal(signal.SIGTSTP, self.empty_signal_handler)


class Encryption(object):

    """
    Class for managing enable password.
    Encrypt with sha256.
    """

    _salt = "IPOT_PTYSH"
    _default_passwd = "5b92b30b5d3e1a6f0dbe1824f4b7b1414bab66396ff0af3b2a329b40c8926146"    # Encrypted string "ptysh"

    def encrypt_passwd(self, passwd):
        return sha256(self._salt.encode() + passwd.encode()).hexdigest()

    def check_passwd(self, passwd):
        return True if self._default_passwd == self.encrypt_passwd(passwd) else False


class LoadModule(object):

    """
    Class for loading submodules.
    """

    def __init__(self, module_path):
        self.module_path = module_path
        self.module_name = self.get_module_name()

    def get_module_name(self):
        """
        Get the name of the module to load.
        Except that the extension is not "py" and the filename is "__init__".
        """
        file_name, file_extension = path.splitext(self.module_path)
        return file_name if file_extension == ".py" and file_name != "__init__" else ""

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
            IoControl().print_message("Module \"%s\" has something problem." % self.module_name)
            IoControl().print_message(e)
            return None

        return self.instance()
