#!/usr/bin/env python

import readline
from ptysh_base import Parser
from ptysh_base import BasicCommand
from ptysh_base import Autocompleter
from ptysh_util import Signal
from ptysh_util import IoControl

def auto_completer(in_text, in_state):
    options = [i for i in Autocompleter().get_cmd_list() if i.startswith(in_text)]
    return options[in_state] if in_state < len(options) else None


def main():
    Signal().set_signal()

    readline.parse_and_bind('tab: complete')
    readline.set_completer(auto_completer)

    io = IoControl()
    io.print_hello_message()

    BasicCommand()

    while True:
        io.set_prompt()
        Parser().parse_command_line(io.get_input_command())


if __name__ == '__main__':
    main()
