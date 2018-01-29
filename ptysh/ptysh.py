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
    option = OptionParser("Usage: %prog ")
    option.add_option("-d", "--dir", dest="conf_dir", type="string", help="PTYSH configuration directory.")

    (options, _) = option.parse_args()

    if options.conf_dir is None:
        return

    Parser().parse_user_input("configure terminal")
    # Do something
    RootNode().switch_enable_mode(False)

def main():
    Signal().init_signal()

    readline.parse_and_bind("tab: complete")
    readline.set_completer(auto_completer)

    IoControl().print_welcome_message()
    RootNode()
    command_line_parser()

    while True:
        user_input = IoControl().get_input_command()
        if len(user_input) == 0:        # Skip input "enter" key.
            continue

        Parser().parse_user_input(user_input)
        Parser().set_auto_completer()


if __name__ == "__main__":
    main()
