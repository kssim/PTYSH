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
        Process the command entered by the user.
        Distinguishes between moving a node and executing a command in a node.
        """
        if Status().current_node != user_input and RootNode().get_module_instance(user_input) is not None:
            # The part moving to the child node.
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
        if Status().module_depth == Status().ROOT_DEPTH:            # base node
            return RootNode().command_set
        elif Status().module_depth == Status().CONFIGURE_DEPTH:     # configure node
            return RootNode().configure_node.command_set
        else:                                                       # module node
            instance = RootNode().get_module_instance(Status().current_node)
            return instance.command_set

    def check_command_set(self, splited_user_input, command_set):
        """
        Ensure that the command entered by the user is included in the node's command set.
        If the command is contained in a node, parse the command.
        """
        for command in command_set:
            if isinstance(command, ModuleCommand):
                return self.check_command_set(splited_user_input, command.command_set)

            if self.parser(splited_user_input, command):
                return True
        return False

    def parser(self, splited_user_input, command):
        """
        Compare user input with stored commands.
        Separate each value with a space and compare by word.
        The argument values are excluded.
        """
        split_stored_command = command.command.split(" ")
        if len(split_stored_command) > len(splited_user_input):
            # The user's input must contain the same value or more than the stored command,
            # because it contains the argument value.
            return False

        if command.workable and splited_user_input[:len(split_stored_command)] == split_stored_command:
            # Check that the commands except the argument match.
            # Then, check whether the command is workable.
            argument_list = splited_user_input[len(split_stored_command):]
            try:
                result = command.handler() if not argument_list else command.handler(argument_list)
            except:
                IoControl().print_message("Invalid command argument")
                return True

            if result == RootNode().EXIT_CODE:
                exit(0)

            return True if result or result is None else False

        return False

    def set_auto_completer(self):
        """
        Registers the commands used in the current node to be autocompleted.
        """
        cmd_set = []
        for command in self.get_command_set():
            cmd_set.append(command.node_name if isinstance(command, ModuleCommand) else command)

        Autocompleter().init_command_set(cmd_set)
