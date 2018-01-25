# -*- coding: utf-8 -*-

"""
A module that describes the basic data structure of each node in the PTYSH.
"""

from inout import IoControl
from structure import Status

class Command(object):

    """
    Basic data structure of command used in PTYSH.
    - command       : Command to use.
    - description   : Description of the command.
    - handler       : Functions to use when executing commands.
    - usage         : Write a usage that will print out an invalid argument value
    - visible       : Whether to show commands in the list.
    - workable      : Whether the command is operational.
    """

    def __init__(self, command, description, handler, usage="", visible=True, workable=True):
        self.command = command
        self.description = description
        self.handler = handler
        self.usage = usage
        self.visible = visible
        self.workable = workable


class ModuleCommand(object):

    """
    Basic data structure for modules to be used in PTYSH.
    The list and exit commands are provided by default.
    - node_name         : The name of the node to be displayed on the configure node.
    - node_description  : Description of the node to be shown on the configure node.
    - command_set       : Commands to use on the node.
    """

    def __init__(self, node_name, node_description, command_set):
        self.node_name = node_name
        self.node_description = node_description

        self.command_set = [
            Command("list", "command list", self.cmd_list),
            Command("exit", "exit", self.cmd_exit)
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
