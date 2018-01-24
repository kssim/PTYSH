import sys
from os import path
from os import listdir
from subprocess import call
from getpass import getpass

from ptysh_util import LoadModule
from ptysh_util import Encryption
from ptysh_util import IoControl
from ptysh_util import Singleton
from ptysh_util import Status

MODULE_PATH = path.join(path.abspath(path.dirname(__file__)), "modules")

class Parser(Singleton):

    def parse_user_input(self, user_input):
        """
        Compares the user's input with the stored command set and finds the command to process.
        Find the result by dividing the input value and command by spaces and comparing them.
        """
        if Status().current_node != user_input and BasicNode().get_module_instance(user_input) is not None:
            Status().increase_module_depth()
            Status().push_current_node(user_input)
            return

        splited_user_input = user_input.split(" ")
        if not self.parse_command_set(splited_user_input, self.get_command_set()):
            io = IoControl()
            io.print_msg("This command(\"%s\") is not supported." % user_input)

    def parse_command_set(self, splited_user_input, command_set):
        for command in command_set:
            if isinstance(command, ModuleCommand):
                return self.parse_command_set(splited_user_input, command.command_set)

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

    def get_command_set(self):
        """
        Get the command set for the current node position.
        """
        if Status().module_depth == Status().ZERO_DEPTH:        # base node
            return BasicNode().command_set
        elif Status().module_depth == Status().CONF_DEPTH:      # configure node
            return BasicNode().configure_terminal.command_set
        else:                                                   # module node
            instance = BasicNode().get_module_instance(Status().current_node)
            return instance.command_set

    def set_auto_completer(self):
        """
        Registers the commands used in the current node to be autocompleted.
        """
        cmd_set = []
        for command in self.get_command_set():
            cmd_set.append(command.node_name if isinstance(command, ModuleCommand) else command)

        Autocompleter().init_command_set(cmd_set)


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
        io = IoControl()

        for command in self.command_set:
            if isinstance(command, ModuleCommand):
                io.print_list(command.node_name, command.node_description)
            elif command.visible:
                io.print_list(command.command, command.description)

    def cmd_exit(self):
        Status().decrease_module_depth()
        Status().pop_current_node()



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
