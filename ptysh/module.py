# -*- coding: utf-8 -*-

"""
"""

from data import Command


class PtyshModule(object):

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

    def add_command(self, in_cmd_name, in_cmd_desc, in_cmd_func, in_hidden_flag, in_working):
        self._command_set.append(Command(in_cmd_name, in_cmd_desc, in_cmd_func, in_hidden_flag, in_working))
