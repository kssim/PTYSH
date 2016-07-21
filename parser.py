from util import Singleton

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

class BasicCommand(object):

    _basic_command = [['list', 'command list', None],
                      ['exit', 'exit', None]]

    def __init__(self):
        self._basic_command[0][2] = self.cmd_list
        self._basic_command[1][2] = self.cmd_exit

    def get_cmd_function(self, command):
        for cmd in self._basic_command:
            if command.strip() == cmd[0].strip():
                return cmd[2]

        return None

    def cmd_list(self):
        for cmd in self._basic_command:
            print ('%s\t\t%s' % (cmd[0], cmd[1]))

    def cmd_exit(self):
        print ('Prgram exit')
        exit(0)
