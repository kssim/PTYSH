from subprocess import call
from getpass import getpass
from ptysh_util import Encryption
from ptysh_util import IoControl
from ptysh_util import Singleton
from ptysh_util import Login

COMMAND_LIST_CMD_IDX = 0
COMMAND_LIST_SHOW_CMD_IDX = 1
COMMAND_LIST_DOC_IDX = 1
COMMAND_LIST_FUNC_IDX = 2
COMMAND_LIST_HIDDEN_IDX = 3

class Parser(Singleton):

    def __init__(self):
        return

    def parse_command_line(self, in_cmd):
        if len(in_cmd) == 1:
            return

        parse_result = BasicCommand().run_command(in_cmd.split(' '))

        if parse_result == False:
            print ('Not support command.')


class BasicCommand(Singleton):

    _basic_command = []

    def __init__(self):
        self._basic_command = [['enable', 'enable mode', self.cmd_enable, False],
                              ['list', 'command list', self.cmd_list, False],
                              ['st', 'start shell', self.cmd_st, True],
                              ['exit', 'exit', self.cmd_exit, False]]

    def run_command(self, in_cmd):
        if in_cmd[COMMAND_LIST_CMD_IDX].strip() == 'show':
            if len(in_cmd) == 1:
                return False

            command = in_cmd[COMMAND_LIST_CMD_IDX].strip() + ' ' + in_cmd[COMMAND_LIST_SHOW_CMD_IDX].strip()
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
        if Login().get_login_state() == True:
            idx = self.get_command_index('enable')
            command = ['disable', 'disable mode', self.cmd_disable, False]
            self.add_login_user_cmd()
        else:
            idx = self.get_command_index('disable')
            command = ['enable', 'enable mode', self.cmd_enable, False]
            self.del_login_user_cmd()

        self._basic_command.pop(idx)
        self._basic_command.insert(0, command)


    def add_login_user_cmd(self):
        if self.get_command_index('show hostname') == -1:
            self._basic_command.append(['show hostname', 'show hostname', self.cmd_show_hostname, False])

    def del_login_user_cmd(self):
        idx = self.get_command_index('show hostname')
        self._basic_command.pop(idx)


    ##### cmd function. #####
    def cmd_enable(self):
        passwd = getpass('password: ')

        en = Encryption()
        if en.validate_passwd(passwd) == False:
            Login().set_login_state(False)
            print ('Failed to enable mode activated.')
            return

        Login().set_login_state(True)
        self.switch_mode()
        print ('Enable mode has been activated.')

    def cmd_disable(self):
        Login().set_login_state(False)
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
