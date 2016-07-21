from sys import stdin
from sys import stdout
from os import path
from getpass import getpass
from ptysh_util import Encryption

HOST_NAME_FILE_PATH = "/etc/hostname"

class IoControl(object):

    _host_name = ""

    def __init__(self):
        self._host_name = self.get_host_name()

    def get_input_command(self):
        return stdin.readline()

    def set_prompt(self, loggined):
        tt = "#" if loggined == True else ">"
        stdout.write(self._host_name + tt + " ")

    def print_hello_message(self):
        message = "Hello, This is Python Teletype Shell.\n"
        message += "COPYRIGHT 2016 IPOT. ALL RIGHTS RESERVED.\n\n"
        stdout.write(message)

    def get_host_name(self):
        if path.exists(HOST_NAME_FILE_PATH) == False:
            return "PTYSH"

        with open(HOST_NAME_FILE_PATH, 'rb') as f:
            return f.readline().strip()


class BasicCommand(object):

    _basic_command = [['en', 'enable mode', None],
                      ['list', 'command list', None],
                      ['exit', 'exit', None]]

    def __init__(self):
        self._basic_command[0][2] = self.cmd_en
        self._basic_command[1][2] = self.cmd_list
        self._basic_command[2][2] = self.cmd_exit

    def get_cmd_function(self, command):
        for cmd in self._basic_command:
            if command.strip() == cmd[0].strip():
                return cmd[2]

        return None

    def cmd_en(self):
        passwd = getpass('password: ')

        en = Encryption()
        if en.validate_passwd(passwd) == True:
            print ('enabled')
        else:
            print ('disabled')


    def cmd_list(self):
        for cmd in self._basic_command:
            print ('%s\t\t%s' % (cmd[0], cmd[1]))

    def cmd_exit(self):
        print ('Prgram exit')
        exit(0)
