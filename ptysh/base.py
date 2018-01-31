# -*- coding: utf-8 -*-

"""
This module controls the basic operation of PTYSH.
It processes root, configure, module nodes, and manages each command.
It also manages the autocomplete list of commands.
"""

import sys
from os import path
from os import listdir
from subprocess import call
from getpass import getpass

from data import Command
from data import ModuleCommand
from inout import IoControl
from utils import LoadModule
from utils import Encryption
from structure import Status
from structure import Singleton

MODULE_PATH = path.join(path.abspath(path.dirname(__file__)), "../modules")


class Autocompleter(Singleton):

    def __init__(self):
        self.command_list = []

    def init_command_set(self, command_list):
        """
        Initialize autocomplete command list.
        """
        del self.command_list[:]    # python2 does not support clear of list.
        for cmd in command_list:
            if type(cmd) == str:                    # node name
                self.command_list.append(cmd)
            elif cmd.visible and cmd.workable:      # command
                self.command_list.append(cmd.command)


class RootNode(Singleton):

    EXIT_CODE = "EXIT"

    def __init__(self):
        self.command_set = [
            Command("enable", "enable mode", self.cmd_enable),
            Command("disable", "disable mode", self.cmd_disable),
            Command("list", "command list", self.cmd_list),
            Command("?", "command list", self.cmd_list, "", False),
            Command("st", "start shell", self.cmd_st, "", False),
            Command("debug", "start ptysh debug mode", self.cmd_debug, "", False),
            Command("show hostname", "show hostname", self.cmd_show_hostname),
            Command("configure terminal", "configure terminal", self.cmd_configure_node),
            Command("refresh", "refresh module list", self.cmd_refresh),
            Command("exit", "exit", self.cmd_exit)
        ]
        Autocompleter().init_command_set(self.command_set)
        self.cmd_refresh()

    def switch_enable_mode(self, enabled):
        """
        Change the commands used in enable and disable modes.
        """
        self.switch_enable_related_command("disable", enabled)
        self.switch_enable_related_command("show hostname", enabled)
        self.switch_enable_related_command("configure terminal", enabled)
        self.switch_enable_related_command("refresh", enabled)
        self.switch_enable_related_command("enable", not enabled)

        Autocompleter().init_command_set(self.command_set)

    def switch_enable_related_command(self, command, status):
        for cmd in self.command_set:
            if cmd.command == command:
                cmd.workable = status

    def init_configure_node(self):
        """
        Initialize nodes and commands used by configure node.
        """
        sys.path.append(MODULE_PATH)
        module_list = listdir(MODULE_PATH)

        module_command_set = []
        for module_name in module_list:
            module = LoadModule(module_name).get_instance()
            if module is None:
                continue

            if self.get_module_instance(module.node_name) is not None:
                IoControl().print_message("Module \"%s\" is duplicated, so do not add it." % module.node_name)
                continue

            module_command_set.append(ModuleCommand(module.node_name, module.node_description, module.command_set))

        self.configure_node = ModuleCommand("configure terminal", "configure terminal", module_command_set)

    def get_module_instance(self, node_name):
        """
        Returns the module object found by the name of the node.
        """
        if self.configure_node is None:
            return None

        for module in self.configure_node.command_set:
            if isinstance(module, ModuleCommand) and module.node_name == node_name:
                return module


    ##### cmd function. #####
    def cmd_enable(self):
        passwd = getpass("password: ")

        encrypt = Encryption()
        if encrypt.check_passwd(passwd):
            Status().login = True
            self.switch_enable_mode(Status().login)
            IoControl().print_message("Enable mode has been activated.")
        else:
            Status().login = False
            IoControl().print_message("Failed to enable mode activated.")

    def cmd_disable(self):
        Status().login = False
        Status().debug = False
        self.switch_enable_mode(Status().login)
        IoControl().print_message("Enable mode has been deactivated.")

    def cmd_st(self):
        passwd = getpass("passwd: ")

        encrypt = Encryption()
        if encrypt.check_passwd(passwd):
            IoControl().print_message("Enter the user shell.")
            call("/bin/bash")
        else:
            IoControl().print_message("Fail to enter the shell.")

    def cmd_debug(self):
        Status().debug = True

    def cmd_list(self):
        for cmd in self.command_set:
            if cmd.visible and cmd.workable:
                IoControl().print_cmd_list(cmd.command, cmd.description)

    def cmd_show_hostname(self):
        IoControl().print_message(IoControl().get_host_name())

    def cmd_configure_node(self):
        Status().increase_module_depth()
        Status().push_current_node("configure terminal")

    def cmd_exit(self):
        Status().debug = False
        IoControl().print_message("Exit ptysh.")
        return self.EXIT_CODE

    def cmd_refresh(self):
        self.configure_node = None
        self.init_configure_node()
