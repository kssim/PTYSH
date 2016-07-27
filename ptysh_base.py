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

MODULE_PATH = './modules/'

COMMAND_LIST_CMD_IDX = 0
COMMAND_LIST_SHOW_CMD_IDX = 1
COMMAND_LIST_CONFIGURE_CMD_IDX = 1
COMMAND_LIST_DOC_IDX = 1
COMMAND_LIST_FUNC_IDX = 2
COMMAND_LIST_HIDDEN_IDX = 3

class Parser(Singleton):

    def parse_command_line(self, in_cmd):
        if len(in_cmd) == 1:    # Skip input 'enter' key.
            return

        parser = ModulesCommand() if Status().get_configure_terminal_state() == True else BasicCommand()
        parse_result = parser.run_command(in_cmd.split(' '))

        if parse_result == False:
            print ('Not support command.')


class Autocompleter(Singleton):

    _cmd_list = []

    def add_cmd(self, cmd):
        self._cmd_list.append(cmd)

    def del_cmd(self, cmd):
        self._cmd_list = [x for x in self._cmd_list if x != cmd]

    def get_cmd_list(self):
        return self._cmd_list


class BasicCommand(Singleton):

    _basic_command = []

    def __init__(self):
        self._basic_command = [['enable', 'enable mode', self.cmd_enable, False],
                              ['list', 'command list', self.cmd_list, False],
                              ['st', 'start shell', self.cmd_st, True],
                              ['exit', 'exit', self.cmd_exit, False]]

        Autocompleter().add_cmd('enable')
        Autocompleter().add_cmd('list')
        Autocompleter().add_cmd('exit')

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
            if command == cmd[COMMAND_LIST_CMD_IDX].strip():
                cmd_function = cmd[COMMAND_LIST_FUNC_IDX]
                cmd_function()
                return True

        return False

    def get_command_index(self, keyword):
        for idx, cmd in enumerate(self._basic_command):
            if keyword in cmd:
                return idx

        return -1

    def switch_mode(self):
        if Status().get_login_state() == True:
            idx = self.get_command_index('enable')
            command = ['disable', 'disable mode', self.cmd_disable, False]
            Autocompleter().add_cmd('disable')
            Autocompleter().del_cmd('enable')
            self.add_login_user_cmd()
        else:
            idx = self.get_command_index('disable')
            command = ['enable', 'enable mode', self.cmd_enable, False]
            Autocompleter().add_cmd('enable')
            Autocompleter().del_cmd('disable')
            self.del_login_user_cmd()

        self._basic_command.pop(idx)
        self._basic_command.insert(0, command)

    def add_login_user_cmd(self):
        if self.get_command_index('show hostname') == -1:
            Autocompleter().add_cmd('show')
            Autocompleter().add_cmd('hostname')
            self._basic_command.append(['show hostname', 'show hostname', self.cmd_show_hostname, False])

            Autocompleter().add_cmd('configure')
            Autocompleter().add_cmd('terminal')
            self._basic_command.append(['configure terminal', 'configure terminal', self.cmd_configure_terminal, False])

    def del_login_user_cmd(self):
        idx = self.get_command_index('show hostname')
        self._basic_command.pop(idx)
        Autocompleter().del_cmd('show')
        Autocompleter().del_cmd('hostname')

        idx = self.get_command_index('configure terminal')
        self._basic_command.pop(idx)
        Autocompleter().del_cmd('configure')
        Autocompleter().del_cmd('terminal')



    ##### cmd function. #####
    def cmd_enable(self):
        passwd = getpass('password: ')

        en = Encryption()
        if en.validate_passwd(passwd) == False:
            Status().set_login_state(False)
            print ('Failed to enable mode activated.')
            return

        Status().set_login_state(True)
        self.switch_mode()
        print ('Enable mode has been activated.')

    def cmd_disable(self):
        Status().set_login_state(False)
        self.switch_mode()
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
            if cmd[COMMAND_LIST_HIDDEN_IDX] == True:
                continue

            print ('%s\t\t%s' % (cmd[COMMAND_LIST_CMD_IDX], cmd[COMMAND_LIST_DOC_IDX]))

    def cmd_exit(self):
        print ('Prgram exit')
        exit(0)

    def cmd_show_hostname(self):
        io = IoControl()
        print io.get_host_name()

    def cmd_configure_terminal(self):
        Status().set_configure_terminal_state(True)
        Autocompleter().del_cmd('configure')
        Autocompleter().del_cmd('terminal')
        Autocompleter().del_cmd('disable')
        Autocompleter().del_cmd('hostname')


class ModulesCommand(Singleton):

    _modules_command = []
    _subnode_modules_command = []

    def __init__(self):
        self._modules_command = [['list', 'command list', self.cmd_list, False],
                              ['exit', 'exit', self.cmd_exit, False]]
        self.init_command()

    def init_command(self):
        sys.path.append(MODULE_PATH)
        modules_list = listdir(MODULE_PATH)

        for module in modules_list:
            file_name, file_extension = path.splitext(module)
            if file_extension != '.py':
                continue

            module = LoadModule(file_name, file_name)
            instance = module.get_instance()
            if instance == None:
                continue

            node_name = instance.get_node_name()
            module_list = instance.get_command_list()

            self._modules_command.append([node_name, module_list])

        if len(self._modules_command) == 0:
            print ('Not usable modules.')
            return

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
                cmd_function()

            return True
        return False

    def cmd_list(self):
        cmd_list = self._subnode_modules_command if Status().get_sub_node() == True else self._modules_command
        for cmd in self._modules_command:
            print ('%s' % cmd[COMMAND_LIST_CMD_IDX])

    def cmd_exit(self):
        Status().set_configure_terminal_state(False)
        Autocompleter().add_cmd('configure')
        Autocompleter().add_cmd('terminal')
        Autocompleter().del_cmd('disable')
        Autocompleter().del_cmd('hostname')
