import dbus
from sys import path
from module import PtyshModule
from structure import Singleton

DBUS_BUS_NAME = "com.kssim.test"
DBUS_OBJECT_PATH = "/com/kssim/test"

class test_module(PtyshModule):

    def __init__(self):
        super(test_module, self).__init__()
        super(test_module, self).init_node("hello", "hello node")
        super(test_module, self).set_dbus_info(DBUS_BUS_NAME, DBUS_OBJECT_PATH, DBUS_BUS_NAME)
        super(test_module, self).add_command("hello", "say hello", self.cmd_print_hello)
        super(test_module, self).add_command("hello_world", "say hello world", self.cmd_print_hello_world)
        super(test_module, self).add_command("argument", "argument", self.cmd_print_argument, "Please enter one or more arguments")
        super(test_module, self).add_command("change_msg", "change print msg", super(test_module, self).dbus_handler, "", False)

    def cmd_print_hello(self):
        print ("hello")

    def cmd_print_hello_world(self):
        print ("hello world")

    def cmd_print_argument(self, arg):
        if len(arg):
            print (arg)
            return True
        return False
