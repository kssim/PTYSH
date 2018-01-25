# -*- coding: utf-8 -*-

"""
"""

import readline

from inout import IoControl
from base import BasicNode
from parser import Parser
from parser import Autocompleter
from utils import Signal


def auto_completer(in_text, in_state):
    options = [i for i in Autocompleter().cmd_set if i.startswith(in_text)]
    return options[in_state] if in_state < len(options) else None


def main():
    Signal().set_signal()

    readline.parse_and_bind('tab: complete')
    readline.set_completer(auto_completer)

    io = IoControl()
    io.print_hello_message()

    BasicNode()

    while True:
        user_input = io.get_input_command()
        if len(user_input) == 0:    # Skip input 'enter' key.
            continue

        Parser().parse_user_input(user_input)
        Parser().set_auto_completer()


if __name__ == '__main__':
    main()
