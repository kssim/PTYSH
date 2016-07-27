from sys import path
path.append('../')
from ptysh_module import PtyshModule

class test_module(PtyshModule):

    def __init__(self):
        PtyshModule.__init__(self)
        PtyshModule.set_node_name(self, 'test')
        PtyshModule.set_command(self, 'hello', 'hello', self.cmd_print_hello, False)

    def cmd_print_hello(self):
        print ('hello')
