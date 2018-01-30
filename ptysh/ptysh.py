# -*- coding: utf-8 -*-

"""
Main module for running ptysh.
"""

import readline
from optparse import OptionParser

from inout import IoControl
from base import RootNode
from parser import Parser
from base import Autocompleter
from utils import Signal


def auto_completer(text, state):
    """
    Handler for autocomplete.
    """
    options = [i for i in Autocompleter().command_list if i.startswith(text)]
    return options[state] if state < len(options) else None

def command_line_parser():
    """
    Functions for parsing PTYSH command options.
    """
    option = OptionParser("Usage: %prog ")
    option.add_option("-l", "--load", dest="load_conf", action="store_true", help="Load the registered module settings of PTYSH.")

    (options, _) = option.parse_args()

    if options.load_conf:
        conf_list = IoControl().get_modules_conf()
        Parser().load_configuration(conf_list)
        exit(0)

def main():
    Signal().init_signal()

    readline.parse_and_bind("tab: complete")
    readline.set_completer(auto_completer)

    RootNode()
    command_line_parser()
    RootNode().switch_enable_mode(False)

    IoControl().print_welcome_message()

    while True:
        user_input = IoControl().get_input_command()
        if len(user_input) == 0:        # Skip input "enter" key.
            continue

        Parser().parse_user_input(user_input)
        Parser().set_auto_completer()


if __name__ == "__main__":
    main()
