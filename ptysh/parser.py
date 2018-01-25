# -*- coding: utf-8 -*-

"""
This module parses the user's input and executes the command on the input.
"""

from inout import IoControl
from base import RootNode
from base import Autocompleter
from data import ModuleCommand
from structure import Status
from structure import Singleton


class Parser(Singleton):

    def parse_user_input(self, user_input):
        """
        Compares the user's input with the stored command set and finds the command to process.
        Find the result by dividing the input value and command by spaces and comparing them.
        """
        if Status().current_node != user_input and RootNode().get_module_instance(user_input) is not None:
            Status().increase_module_depth()
            Status().push_current_node(user_input)
            return

        splited_user_input = user_input.split(" ")
        if not self.check_command_set(splited_user_input, self.get_command_set()):
            IoControl().print_message("This command(\"%s\") is not supported." % user_input)

    def get_command_set(self):
        """
        Get the command set for the current node position.
        """
        if Status().module_depth == Status().ZERO_DEPTH:            # base node
            return RootNode().command_set
        elif Status().module_depth == Status().CONFIGURE_DEPTH:     # configure node
            return RootNode().configure_node.command_set
        else:                                                       # module node
            instance = RootNode().get_module_instance(Status().current_node)
            return instance.command_set

    def check_command_set(self, splited_user_input, command_set):
        for command in command_set:
            if isinstance(command, ModuleCommand):
                return self.check_command_set(splited_user_input, command.command_set)

            if self.parser(splited_user_input, command):
                return True
        return False

    def parser(self, splited_user_input, command):
        split_stored_command = command.command.split(" ")
        if len(splited_user_input) > len(split_stored_command):
            # The user's input must contain the same value or more than the stored command,
            # because it contains the argument value.
            return False

        if command.workable and splited_user_input[:len(split_stored_command)] == split_stored_command:
            # Make sure that the commands except the arguments are matched and must be workable command.
            command.handler()
            return True
        return False

    def set_auto_completer(self):
        """
        Registers the commands used in the current node to be autocompleted.
        """
        cmd_set = []
        for command in self.get_command_set():
            cmd_set.append(command.node_name if isinstance(command, ModuleCommand) else command)

        Autocompleter().init_command_set(cmd_set)