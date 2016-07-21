from sys import stdin
from sys import stdout
from os import path

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
