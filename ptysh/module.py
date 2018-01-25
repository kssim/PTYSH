# -*- coding: utf-8 -*-

"""
Interface module when developing PTYSH module.
"""

from data import Command


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

    @node_name.setter
    def node_name(self, node_name):
        self._node_name = node_name

    @property
    def node_description(self):
        return self._node_description

    @node_description.setter
    def node_description(self, node_description):
        self._node_description = node_description

    @property
    def command_set(self):
        return self._command_set

    def add_command(self, command_name, command_desc, command_function, visible, workable):
        self._command_set.append(Command(command_name, command_desc, command_function, visible, workable))
