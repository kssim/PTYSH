#!/usr/bin/env python

from ptysh_base import Parser
from ptysh_util import IoControl
from ptysh_util import Signal

def main():
    Signal().set_signal()

    io = IoControl()
    io.print_hello_message()

    while True:
        io.set_prompt()
        Parser().parse_command_line(io.get_input_command())


if __name__ == '__main__':
    main()
