from ptysh_util import Singleton
from ptysh_base import BasicCommand

class Parser(Singleton):

    def __init__(self):
        return

    def parse_command_line(self, in_cmd):
        parse_result = BasicCommand().run_command(in_cmd.split(' '))

        if parse_result == False:
            print ('Not support command.')
