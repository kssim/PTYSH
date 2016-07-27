from sys import path
path.append('../')
from ptysh_module import PtyshModule
from ptysh_util import Singleton
from ptysh_base import Autocompleter

class test_module(PtyshModule, Singleton):

    def __init__(self):
        PtyshModule.__init__(self)
        PtyshModule.set_node_name(self, 'test')
        PtyshModule.set_command(self, 'hello', 'hello', self.cmd_print_hello, False)

    def cmd_print_hello(self):
        print ('hello')
