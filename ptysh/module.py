# -*- coding: utf-8 -*-

"""
Interface module when developing PTYSH module.
"""

from data import Command
from inout import IoControl
from structure import Status
from structure import PtyshDbus

class PtyshModule(object):

    """
    Interfaces required when developing a node in a child module
    The child module inherits this interface and implements the node's name, description, and command.
    """

    def __init__(self):
        self._node_name = ""
        self._node_description = ""
        self._command_set = []

    @property
    def node_name(self):
        return self._node_name

    @property
    def node_description(self):
        return self._node_description

    def init_node(self, node_name, node_description):
        self._node_name = node_name
        self._node_description = node_description

    @property
    def command_set(self):
        return self._command_set

    def add_command(self, command_name, command_desc, command_function, usage="", visible=True, workable=True):
        self._command_set.append(Command(command_name, command_desc, command_function, usage, visible, workable))

    def get_dbus(self, service_name, object_path):
        return PtyshDbus(service_name, object_path)



