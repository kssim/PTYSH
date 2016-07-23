from sys import stdin
from sys import stdout
from os import path
from getpass import getpass
from ptysh_util import Encryption
from ptysh_util import Singleton
from ptysh_util import Login

HOST_NAME_FILE_PATH = '/etc/hostname'
COMMAND_LIST_CMD_IDX = 0
COMMAND_LIST_DOC_IDX = 1
COMMAND_LIST_FUNC_IDX = 2

class IoControl(object):

    _host_name = ''

    def __init__(self):
        self._host_name = self.get_host_name()

    def get_input_command(self):
        return stdin.readline()

    def set_prompt(self):
        tt = '#' if Login().get_login_state() == True else '>'
        stdout.write(self._host_name + tt + ' ')

    def print_hello_message(self):
        message = 'Hello, This is Python Teletype Shell.\n'
        message += 'COPYRIGHT 2016 IPOT. ALL RIGHTS RESERVED.\n\n'
        stdout.write(message)

    def get_host_name(self):
        if path.exists(HOST_NAME_FILE_PATH) == False:
            return 'PTYSH'

        with open(HOST_NAME_FILE_PATH, 'rb') as f:
            return f.readline().strip()


class BasicCommand(Singleton):

    _basic_command = []

    def __init__(self):
        self._basic_command = [['en', 'enable mode', self.cmd_en],
                              ['list', 'command list', self.cmd_list],
                              ['exit', 'exit', self.cmd_exit]]

    def run_command(self, in_cmd):
        if in_cmd[0].strip() == 'show':
            command = in_cmd[0].strip() + ' ' + in_cmd[1].strip()
        else:
            command = in_cmd[0].strip()


        for cmd in self._basic_command:
            if command == cmd[COMMAND_LIST_CMD_IDX].strip():
                cmd_function = cmd[COMMAND_LIST_FUNC_IDX]
                cmd_function()
                return True

        return False

    def add_private_command(self):
        self._basic_command.append(['show hostname', 'show hostname', self.cmd_show_hostname])


    ##### cmd function. #####
    def cmd_en(self):
        passwd = getpass('password: ')

        en = Encryption()
        if en.validate_passwd(passwd) == False:
            Login().set_login_state(False)
            print ('Failed to enable mode activated.')
            return

        Login().set_login_state(True)
        self.add_private_command()
        print ('Enable mode has been activated.')

    def cmd_list(self):
        for cmd in self._basic_command:
            print ('%s\t\t%s' % (cmd[COMMAND_LIST_CMD_IDX], cmd[COMMAND_LIST_DOC_IDX]))

    def cmd_exit(self):
        print ('Prgram exit')
        exit(0)

    def cmd_show_hostname(self):
        io = IoControl()
        print io.get_host_name()
