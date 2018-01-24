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
PRINT_FORMAT_PADDING = 30

class Parser(Singleton):

    def parse_user_input(self, user_input):
        """
        Compares the user's input with the stored command set and finds the command to process.
        Find the result by dividing the input value and command by spaces and comparing them.
        """
        if Status().current_node != user_input and ModuleNode().get_module_instance(user_input) is not None:
            Status().increase_module_depth()
            Status().push_current_node(user_input)
            return

        splited_user_input = user_input.split(" ")
        if not self.parse_command_set(splited_user_input, self.get_command_set()):
            print ("This command is not supported.")

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
        if not Status().configure:                              # base node
            return BasicNode().command_set
        elif Status().module_depth == Status().ZERO_DEPTH :      # configure node
            return ModuleNode().command_set
        else:                                                   # module node
            instance = ModuleNode().get_module_instance(Status().current_node)
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
        for command in self.command_set:
            if isinstance(command, ModuleCommand):
                print ("  %s%s" % (command.node_name, command.node_description))
            elif command.visible:
                print ("  %s%s" % (command.command.ljust(PRINT_FORMAT_PADDING), command.description))

    def cmd_exit(self):
        Status().decrease_module_depth()
        Status().pop_current_node()



class BasicNode(Singleton):

    def __init__(self):
        self.command_set = [
            Command("enable", "enable mode", self.cmd_enable, True, True),
            Command("disable", "disable mode", self.cmd_disable, True, False),
            Command("list", "command list", self.cmd_list, True, True),
            Command("st", "start shell", self.cmd_st, False, True),
            Command("show hostname", "show hostname", self.cmd_show_hostname, True, False),
            Command("configure terminal", "configure terminal", self.cmd_configure_terminal, True, False),
            Command("exit", "exit", self.cmd_exit, True, True)
        ]
        Autocompleter().init_command_set(self.command_set)

    def switch_cmd_working_state(self, command, status):
        for cmd in self.command_set:
            if cmd.command == command:
                cmd.workable = status

    def switch_login_mode(self):
        show_logined_cmd = getattr(Status(), "login")
        self.switch_cmd_working_state("disable", show_logined_cmd)
        self.switch_cmd_working_state("show hostname", show_logined_cmd)
        self.switch_cmd_working_state("configure terminal", show_logined_cmd)
        self.switch_cmd_working_state("enable", not show_logined_cmd)

        Autocompleter().init_command_set(self.command_set)


    ##### cmd function. #####
    def cmd_enable(self):
        passwd = getpass("password: ")

        en = Encryption()
        if en.validate_passwd(passwd) == False:
            Status().login = False
            print ("Failed to enable mode activated.")
            return

        Status().login = True
        self.switch_login_mode()
        print ("Enable mode has been activated.")

    def cmd_disable(self):
        Status().login = False
        self.switch_login_mode()
        print ("Enable mode has been deactivated.")

    def cmd_st(self):
        passwd = getpass("passwd: ")

        en = Encryption()
        if en.validate_passwd(passwd) == False:
            print ("Fail to enter the shell.")
            return

        print ("Enter the user shell.")
        call("/bin/bash")

    def cmd_list(self):
        for cmd in self.command_set:
            if cmd.visible == False or cmd.workable == False:
                continue

            print ("  %s%s" % (cmd.command.ljust(PRINT_FORMAT_PADDING), cmd.description))

    def cmd_exit(self):
        print ("Program exit")
        exit(0)

    def cmd_show_hostname(self):
        io = IoControl()
        print (io.get_host_name())

    def cmd_configure_terminal(self):
        Status().configure = True


class ModuleNode(Singleton):

    def __init__(self):
        self._command_set = [
            Command("list", "command list", self.cmd_list, True, True),
            Command("refresh", "refresh module list", self.cmd_refresh, True, True),
            Command("exit", "exit", self.cmd_exit, True, True)
        ]
        self._module_command_set = []
        self.cmd_refresh()

    @property
    def command_set(self):
        return self._command_set + self._module_command_set

    @property
    def module_command_set(self):
        return self._module_command_set

    def init_module_command(self):
        """
        Loads the module information and initializes the node name and command
        of the module to be registered in the CLI.
        """
        sys.path.append(MODULE_PATH)
        modules_list = listdir(MODULE_PATH)

        for module_name in modules_list:
            instance = LoadModule(module_name).get_instance()
            if instance is None:
                continue

            node_name = instance.node_name
            if self.get_module_instance(node_name) is not None:
                print ("Module \"%s\" is redundant, so do not add it." % node_name)
                continue

            self._module_command_set.append(ModuleCommand(node_name, instance.node_description, instance.command_set))

    def get_module_instance(self, node_name):
        for module in self._module_command_set:
            if module.node_name == node_name:
                return module

    def get_node_names(self):
        return [(module.node_name, module.node_description) for module in self._module_command_set]


    ##### cmd function. #####
    def cmd_list(self):
        for cmd in self._command_set:
            print ("  %s%s" % (cmd.command.ljust(PRINT_FORMAT_PADDING), cmd.description))

        for node_name, node_description in self.get_node_names():
            print ("  %s%s" % (node_name.ljust(PRINT_FORMAT_PADDING), node_description))

    def cmd_exit(self):
        Status().configure = False

    def cmd_refresh(self):
        self._module_command_set = []
        self.init_module_command()
