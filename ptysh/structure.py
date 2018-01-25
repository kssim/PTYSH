# -*- coding: utf-8 -*-

"""
Modules related to structure used throughout PTYSH.
"""


class _Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton("Singleton", (object,), {})): pass


class Status(Singleton):

    """
    Class for checking status in PTYSH
    You can check the login(enable) status, the depth of the node, and the name of the node.
    """

    ROOT_DEPTH = 0
    CONFIGURE_DEPTH = 1

    def __init__(self):
        self._login = False
        self._module_depth = self.ROOT_DEPTH
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
