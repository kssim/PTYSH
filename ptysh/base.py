# -*- coding: utf-8 -*-

"""
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
        self.cmd_set = []

    def init_command_set(self, cmd_set):
        """
        Initialize autocomplete command set.
        """
        del self.cmd_set[:]     # python2 does not support clear of list.
        for cmd in cmd_set:
            if type(cmd) == str:
                self.cmd_set.append(cmd)
            elif cmd.visible and cmd.workable:
                self.cmd_set.append(cmd.command)


class BasicNode(Singleton):

    def __init__(self):
        self.io = IoControl()
        self.command_set = [
            Command("enable", "enable mode", self.cmd_enable, True, True),
            Command("disable", "disable mode", self.cmd_disable, True, False),
            Command("list", "command list", self.cmd_list, True, True),
            Command("st", "start shell", self.cmd_st, False, True),
            Command("show hostname", "show hostname", self.cmd_show_hostname, True, False),
            Command("configure terminal", "configure terminal", self.cmd_configure_terminal, True, False),
            Command("refresh", "refresh module list", self.cmd_refresh, True, False),
            Command("exit", "exit", self.cmd_exit, True, True)
        ]
        self.configure_terminal = None
        self.init_configure_terminal()
        Autocompleter().init_command_set(self.command_set)

    def switch_cmd_working_state(self, command, status):
        for cmd in self.command_set:
            if cmd.command == command:
                cmd.workable = status

    def switch_login_mode(self):
        show_logined_view = getattr(Status(), "login")
        self.switch_cmd_working_state("disable", show_logined_view)
        self.switch_cmd_working_state("show hostname", show_logined_view)
        self.switch_cmd_working_state("configure terminal", show_logined_view)
        self.switch_cmd_working_state("refresh", show_logined_view)
        self.switch_cmd_working_state("enable", not show_logined_view)

        Autocompleter().init_command_set(self.command_set)

    def init_configure_terminal(self):
        sys.path.append(MODULE_PATH)
        module_list = listdir(MODULE_PATH)

        module_set = []
        for module_name in module_list:
            instance = LoadModule(module_name).get_instance()
            if instance is None:
                continue

            node_name = instance.node_name
            if self.get_module_instance(node_name) is not None:
                self.io.print_msg("Module \"%s\" is redundant, so do not add it." % node_name)
                continue

            module_set.append(ModuleCommand(node_name, instance.node_description, instance.command_set))

        self.configure_terminal = ModuleCommand("configure terminal", "configure terminal", module_set)

    def get_module_instance(self, node_name):
        if self.configure_terminal is None:
            return None

        for module in self.configure_terminal.command_set:
            if isinstance(module, ModuleCommand) and module.node_name == node_name:
                return module


    ##### cmd function. #####
    def cmd_enable(self):
        passwd = getpass("password: ")

        en = Encryption()
        if en.validate_passwd(passwd) == False:
            Status().login = False
            self.io.print_msg("Failed to enable mode activated.")
            return

        Status().login = True
        self.switch_login_mode()
        self.io.print_msg("Enable mode has been activated.")

    def cmd_disable(self):
        Status().login = False
        self.switch_login_mode()
        self.io.print_msg("Enable mode has been deactivated.")

    def cmd_st(self):
        passwd = getpass("passwd: ")

        en = Encryption()
        if en.validate_passwd(passwd) == False:
            self.io.print_msg("Fail to enter the shell.")
            return

        self.io.print_msg("Enter the user shell.")
        call("/bin/bash")

    def cmd_list(self):
        for cmd in self.command_set:
            if cmd.visible == False or cmd.workable == False:
                continue

            self.io.print_list(cmd.command, cmd.description)

    def cmd_exit(self):
        self.io.print_msg("Program exit")
        exit(0)

    def cmd_show_hostname(self):
        self.io.print_msg(self.io.get_host_name())

    def cmd_configure_terminal(self):
        Status().increase_module_depth()
        Status().push_current_node("configure terminal")

    def cmd_refresh(self):
        pass
