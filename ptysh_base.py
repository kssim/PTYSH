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

MODULE_PATH = path.join(path.abspath(path.dirname(__file__)), 'modules')

COMMAND_LIST_CMD_IDX = 0
COMMAND_LIST_SHOW_CMD_IDX = 1
COMMAND_LIST_CONFIGURE_CMD_IDX = 1
COMMAND_LIST_DOC_IDX = 1
COMMAND_LIST_FUNC_IDX = 2
COMMAND_LIST_HIDDEN_IDX = 3
COMMAND_LIST_WORKING_IDX = 4

PRINT_FORMAT_PADDING = 30

class Parser(Singleton):

    def parse_command_line(self, in_cmd):
        if len(in_cmd) == 0:    # Skip input 'enter' key.
            return

        parser = ModulesCommand() if Status().get_configure_terminal_state() == True else BasicCommand()
        parse_result = parser.run_command(in_cmd.split(' '))

        if parse_result == False:
            print ('Not support command.')

        ModulesCommand().set_autocompleter()
        BasicCommand().set_autocompleter()


class Autocompleter(Singleton):

    _cmd_list = []

    def get_cmd_list(self):
        return self._cmd_list

    def add_cmd_list(self, in_cmd_list):
        for cmd in in_cmd_list:
            if len(cmd) > 4 and cmd[COMMAND_LIST_WORKING_IDX] == False:
                # Exception code.
                # 'configure terminal' modules list has only two cmd items.
                # So, skip the 'configure terminal' modules list.
                continue

            self._cmd_list.append(cmd[COMMAND_LIST_CMD_IDX])

    def del_cmd_list(self, in_cmd_list):
        for cmd in in_cmd_list:
            self._cmd_list = [x for x in self._cmd_list if x != cmd[COMMAND_LIST_CMD_IDX]]


class BasicCommand(Singleton):

    _basic_command = []

    def __init__(self):
        self._basic_command = [['enable', 'enable mode', self.cmd_enable, False, True],
                              ['disable', 'disable mode', self.cmd_disable, False, False],
                              ['list', 'command list', self.cmd_list, False, True],
                              ['st', 'start shell', self.cmd_st, True, True],
                              ['show hostname', 'show hostname', self.cmd_show_hostname, False, False],
                              ['configure terminal', 'configure terminal', self.cmd_configure_terminal, False, False],
                              ['exit', 'exit', self.cmd_exit, False, True]]
        Autocompleter().add_cmd_list(self._basic_command)

    def set_autocompleter(self):
        if Status().get_configure_terminal_state() == True:
            return

        Autocompleter().add_cmd_list(self._basic_command)

    def run_command(self, in_cmd):
        if in_cmd[COMMAND_LIST_CMD_IDX].strip() == 'show':
            if len(in_cmd) == 1:
                return False

            command = in_cmd[COMMAND_LIST_CMD_IDX].strip() + ' ' + in_cmd[COMMAND_LIST_SHOW_CMD_IDX].strip()
        elif in_cmd[COMMAND_LIST_CMD_IDX].strip() == 'configure':
            if len(in_cmd) == 1:
                return False

            if in_cmd[COMMAND_LIST_CONFIGURE_CMD_IDX].strip() != 'terminal':
                return False

            command = in_cmd[COMMAND_LIST_CMD_IDX].strip() + ' ' + in_cmd[COMMAND_LIST_CONFIGURE_CMD_IDX].strip()
        else:
            command = in_cmd[COMMAND_LIST_CMD_IDX].strip()


        for cmd in self._basic_command:
            if command == cmd[COMMAND_LIST_CMD_IDX].strip() and cmd[COMMAND_LIST_WORKING_IDX] == True:
                cmd_function = cmd[COMMAND_LIST_FUNC_IDX]
                cmd_function()
                return True

        return False

    def switch_cmd_working_state(self, in_keyword, in_working_state):
        for cmd in self._basic_command:
            if in_keyword == cmd[COMMAND_LIST_CMD_IDX].strip():
                cmd[COMMAND_LIST_WORKING_IDX] = in_working_state

    def switch_login_mode(self):
        logined = Status().get_login_state()
        self.switch_cmd_working_state('disable', logined)
        self.switch_cmd_working_state('show hostname', logined)
        self.switch_cmd_working_state('configure terminal', logined)
        self.switch_cmd_working_state('enable', not logined)

        Autocompleter().del_cmd_list(self._basic_command)
        Autocompleter().add_cmd_list(self._basic_command)


    ##### cmd function. #####
    def cmd_enable(self):
        passwd = getpass('password: ')

        en = Encryption()
        if en.validate_passwd(passwd) == False:
            Status().set_login_state(False)
            print ('Failed to enable mode activated.')
            return

        Status().set_login_state(True)
        self.switch_login_mode()
        print ('Enable mode has been activated.')

    def cmd_disable(self):
        Status().set_login_state(False)
        self.switch_login_mode()
        print ('Enable mode has been deactivated.')

    def cmd_st(self):
        passwd = getpass('passwd: ')

        en = Encryption()
        if en.validate_passwd(passwd) == False:
            print ('Fail to enter the shell.')
            return

        print ('Enter the user shell.')
        call('/bin/bash')

    def cmd_list(self):
        for cmd in self._basic_command:
            if cmd[COMMAND_LIST_HIDDEN_IDX] == True or cmd[COMMAND_LIST_WORKING_IDX] == False:
                continue

            print ('%s%s' % (cmd[COMMAND_LIST_CMD_IDX].ljust(PRINT_FORMAT_PADDING), cmd[COMMAND_LIST_DOC_IDX]))

    def cmd_exit(self):
        print ('Program exit')
        exit(0)

    def cmd_show_hostname(self):
        io = IoControl()
        print (io.get_host_name())

    def cmd_configure_terminal(self):
        Status().set_configure_terminal_state(True)
        Autocompleter().del_cmd_list(self._basic_command)


class ModulesCommand(Singleton):

    _modules_command = []
    _subnode_modules_command = []

    def __init__(self):
        self.cmd_refresh()

    def init_basic_command(self):
        self._modules_command = [['list', 'command list', self.cmd_list, False, True],
                              ['refresh', 'refresh module list', self.cmd_refresh, False, True],
                              ['exit', 'exit', self.cmd_exit, False, True]]

    def init_command(self):
        sys.path.append(MODULE_PATH)
        modules_list = listdir(MODULE_PATH)

        for module in modules_list:
            file_name, file_extension = path.splitext(module)
            if file_extension != '.py' or file_name == '__init__':
                continue

            try:
                module = LoadModule(file_name, file_name)
                instance = module.get_instance()
            except:
                print ('Your module(\'%s\') has a problem.' % file_name)
                print ('Please check your module\'s file name and class name.')
                continue
            else:
                if instance == None:
                    continue

                node_name = instance.get_node_name()
                module_list = instance.get_command_list()


            if self.module_cmd_duplicate_check(node_name) == True:
                print ('\'%s\' module name is duplicated, so this module is not added.' % file_name)
                continue

            self._modules_command.append([node_name, module_list])

        if len(self._modules_command) == 0:
            print ('Not usable modules.')
            return

    def module_cmd_duplicate_check(self, key):
        for module in self._modules_command:
            if key in module:
                return True
        return False

    def set_autocompleter(self):
        if Status().get_sub_node() == True:
            Autocompleter().add_cmd_list(self._subnode_modules_command)
        else:
            Autocompleter().del_cmd_list(self._subnode_modules_command)

        if Status().get_configure_terminal_state() == True:
            Autocompleter().add_cmd_list(self._modules_command)
        else:
            Autocompleter().del_cmd_list(self._modules_command)


    def run_command(self, in_cmd):
        command = in_cmd[COMMAND_LIST_CMD_IDX].strip()

        cmd_list = self._subnode_modules_command if Status().get_sub_node() == True else self._modules_command
        for cmd in cmd_list:
            if command != cmd[COMMAND_LIST_CMD_IDX].strip():
                continue

            if len(cmd) == 2:                                   # submodules list count (module_name, module_command_list)
                Status().set_sub_node(True)
                Status().set_current_node(cmd[0])               # module_name index
                self._subnode_modules_command = cmd[1]          # modules_command_list index
            else:
                cmd_function = cmd[COMMAND_LIST_FUNC_IDX]
                try:
                    cmd_function(*in_cmd[1:])                   # pass arguments and skip command.
                except:
                    print ("This command is not supported.")

            return True
        return False



    ##### cmd function. #####
    def cmd_list(self):
        cmd_list = self._subnode_modules_command if Status().get_sub_node() == True else self._modules_command
        for cmd in self._modules_command:
            print ('%s' % cmd[COMMAND_LIST_CMD_IDX].ljust(PRINT_FORMAT_PADDING))

    def cmd_exit(self):
        Status().set_configure_terminal_state(False)
        self.set_autocompleter()

    def cmd_refresh(self):
        self.init_basic_command()
        self.init_command()
        self.set_autocompleter()
