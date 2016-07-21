#!/usr/bin/env python

from io_control import IoControl
from parser import Parser
from util import Signal

def main():
    loggined = False

    Signal().set_signal()

    io = IoControl()
    io.print_hello_message()

    while True:
        io.set_prompt(loggined)
        Parser().parse_command_line(io.get_input_command())


if __name__ == '__main__':
    main()
