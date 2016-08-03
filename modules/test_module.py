import dbus
from sys import path
from ptysh_module import PtyshModule
from ptysh_util import Singleton

DBUS_BUS_NAME = 'com.kssim.test'
DBUS_OBJECT_PATH = '/com/kssim/test'

class test_module(PtyshModule, Singleton):

    def __init__(self):
        PtyshModule.__init__(self)
        PtyshModule.set_node_name(self, 'hello')
        PtyshModule.set_command(self, 'hello', 'say hello', self.cmd_print_hello, False, True)
        PtyshModule.set_command(self, 'hello_world', 'say hello world', self.cmd_print_hello_world, True, True)
        PtyshModule.set_command(self, 'change_msg', 'change print msg', self.cmd_send_msg_to_daemon, False, True)

    def cmd_print_hello(self):
        print ('hello')

    def cmd_print_hello_world(self):
        print ('hello world')

    def cmd_send_msg_to_daemon(self, in_msg):
        try:
            bus = dbus.SystemBus()
            bus_object = bus.get_object(DBUS_BUS_NAME, DBUS_OBJECT_PATH)
            bus_interface = dbus.Interface(bus_object, DBUS_BUS_NAME)

            bus_interface.receive_signal(in_msg)
        except:
            print ('The daemon is not loaded.')
