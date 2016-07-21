from ptysh_util import Singleton
from ptysh_base import BasicCommand

class Parser(Singleton):

    def __init__(self):
        return

    def parse_command_line(self, command):
        analyze_command = command.split(' ')
        commander = BasicCommand()

        command_function = commander.get_cmd_function(analyze_command[0])

        if command_function != None:
            command_function()
            return

        print command
