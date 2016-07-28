from sys import path
path.append('../')
from ptysh_module import PtyshModule
from ptysh_util import Singleton

class test_module(PtyshModule, Singleton):

    def __init__(self):
        PtyshModule.__init__(self)
        PtyshModule.set_node_name(self, 'hello')
        PtyshModule.set_command(self, 'hello', 'say hello', self.cmd_print_hello, False, True)
        PtyshModule.set_command(self, 'world', 'say world', self.cmd_print_world, False, True)
        PtyshModule.set_command(self, 'hello_world', 'say hello world', self.cmd_print_hello_world, True, True)

    def cmd_print_hello(self):
        print ('hello')

    def cmd_print_world(self):
        print ('world')

    def cmd_print_hello_world(self):
        print ('hello world')
