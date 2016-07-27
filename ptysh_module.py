from ptysh_util import Status

class PtyshModule(object):

    _node_name = ''
    _command_list = []

    def __init__(self):
        self._command_list = [['exit', 'exit', self.cmd_exit, False],
                              ['list', 'list', self.cmd_list, False]]

    def get_node_name(self):
        return self._node_name

    def set_node_name(self, in_node_name):
        self._node_name = in_node_name

    def get_command_list(self):
        return self._command_list

    def set_command(self, in_cmd_name, in_cmd_desc, in_cmd_func, in_hidden_flag):
        self._command_list.append([in_cmd_name, in_cmd_desc, in_cmd_func, in_hidden_flag])

    def cmd_exit(self):
        Status().set_sub_node(False)

    def cmd_list(self):
        for cmd in self._command_list:
            print ('%s\t\t%s' % (cmd[0], cmd[1]))
