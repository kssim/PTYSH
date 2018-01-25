# -*- coding: utf-8 -*-

"""
"""

import sys
from os import path

from structure import Status

HOST_NAME_FILE_PATH = '/etc/hostname'


class IoControl(object):

    def __init__(self):
        self._host_name = self.get_host_name()

    def get_input_command(self):
        prompt_msg = self.get_prompt_msg()
        return input(prompt_msg) if sys.version_info >= (3,0) else raw_input(prompt_msg)

    def get_host_name(self):
        if path.exists(HOST_NAME_FILE_PATH) == False:
            return "PTYSH"          # default prompt name

        with open(HOST_NAME_FILE_PATH, "rb") as f:
            return f.readline().strip()

    def get_prompt_msg(self):
        prompt = "#" if Status().login else ">"

        if Status().module_depth > Status().ZERO_DEPTH:
            location = "(%s)" % Status().current_node
        else:
            location = ""

        formatted_prompt = "%s%s%s " % (self._host_name.decode('utf-8'), location, prompt)
        return formatted_prompt

    def print_hello_message(self):
        message = "Hello, This is Python Teletype Shell.\n"
        message += "COPYRIGHT 2017 KyeongSeob Sim. ALL RIGHTS RESERVED.\n"
        self.print_msg(message)

    def print_list(self, command, description):
        self.print_msg("  %s%s" % (command.ljust(30), description))

    def print_msg(self, msg):
        print (msg)
