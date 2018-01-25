import dbus
from sys import path
from module import PtyshModule
from structure import Singleton

DBUS_BUS_NAME = "com.kssim.test"
DBUS_OBJECT_PATH = "/com/kssim/test"

class test_module(PtyshModule, Singleton):

    def __init__(self):
        PtyshModule.__init__(self)
        PtyshModule.node_name = "hello"
        PtyshModule.node_description = "hello node"
        PtyshModule.add_command(self, "hello", "say hello", self.cmd_print_hello)
        PtyshModule.add_command(self, "hello_world", "say hello world", self.cmd_print_hello_world)
        PtyshModule.add_command(self, "argument", "argument", self.cmd_print_argument, "Please enter one or more arguments")
        PtyshModule.add_command(self, "change_msg", "change print msg", self.cmd_send_msg_to_daemon, "", False)

    def cmd_print_hello(self):
        print ("hello")

    def cmd_print_hello_world(self):
        print ("hello world")

    def cmd_print_argument(self, arg):
        if len(arg):
            print (arg)
            return True
        return False

    def cmd_send_msg_to_daemon(self, in_msg):
        try:
            bus = dbus.SystemBus()
            bus_object = bus.get_object(DBUS_BUS_NAME, DBUS_OBJECT_PATH)
            bus_interface = dbus.Interface(bus_object, DBUS_BUS_NAME)

            bus_interface.receive_signal(in_msg)
        except:
            print ("The daemon is not loaded.")
