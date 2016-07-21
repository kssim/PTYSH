#!/usr/bin/env python

from io_control import IoControl
from parser import Parser

def main():
    loggined = False

    io = IoControl()
    io.print_hello_message()

    while True:
        io.set_prompt(loggined)
        Parser().command_parser(io.get_input_command())



if __name__ == '__main__':
    main()
