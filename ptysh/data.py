# -*- coding: utf-8 -*-

"""
A module that describes the basic data structure of each node in the CLI.
"""

from inout import IoControl
from structure import Status

class Command(object):

    def __init__(self, command, description, handler, visible=True, workable=True):
        self.command = command
        self.description = description
        self.handler = handler
        self.visible = visible
        self.workable = workable


class ModuleCommand(object):

    def __init__(self, node_name, node_description, command_set):
        self.node_name = node_name
        self.node_description = node_description

        self.command_set = [
            Command("list", "command list", self.cmd_list, True, True),
            Command("exit", "exit", self.cmd_exit, True, True)
        ]
        self.command_set += command_set


    ##### cmd function. #####
    def cmd_list(self):
        for command in self.command_set:
            if isinstance(command, ModuleCommand):
                IoControl().print_cmd_list(command.node_name, command.node_description)
            elif command.visible:
                IoControl().print_cmd_list(command.command, command.description)

    def cmd_exit(self):
        Status().decrease_module_depth()
        Status().pop_current_node()
