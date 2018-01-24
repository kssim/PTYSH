from ptysh_util import Status
from ptysh_base import Command

PRINT_FORMAT_LEFT_PADDING   = 30

class PtyshModule(object):

    def __init__(self):
        self._node_name = ""

        # command list
        # - [command, description, function, invisible state, workable state]
        self._command_set = [
            Command("exit", "exit", self.cmd_exit, False, True),
            Command("list", "command list", self.cmd_list, False, True)
        ]

    @property
    def node_name(self):
        return self._node_name

    @node_name.setter
    def node_name(self, node_name):
        self._node_name = node_name

    @property
    def command_set(self):
        return self._command_set

    def set_command(self, in_cmd_name, in_cmd_desc, in_cmd_func, in_hidden_flag, in_working):
        self._command_set.append(Command(in_cmd_name, in_cmd_desc, in_cmd_func, in_hidden_flag, in_working))

    def cmd_exit(self):
        Status().module = False

    def cmd_list(self):
        for cmd in self._command_set:
            if cmd.visible == False or cmd.workable == False:
                # invisible state is true and workable state is false.
                continue

            print ('%s%s' % (cmd.command.ljust(PRINT_FORMAT_LEFT_PADDING), cmd.description))   # print command name and description.
