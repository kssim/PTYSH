import dbus
from sys import path
from module import PtyshModule
from structure import Singleton

HOSTNAME_SERVICE_NAME = "org.freedesktop.hostname1"
HOSTNAME_OBJECT_PATH = "/org/freedesktop/hostname1"
HOSTNAME_INTERFACE = "org.freedesktop.hostname1"

DBUS_BUS_NAME = "com.kssim.test"
DBUS_OBJECT_PATH = "/com/kssim/test"

class test_module(PtyshModule):

    welcome_msg = "empty"

    def __init__(self):
        super(test_module, self).__init__()
        super(test_module, self).init_node("hello", "hello node")

        super(test_module, self).add_command("show hello_world", "show hello world", self.cmd_show_hello_world)
        super(test_module, self).add_command("show hello", "show hello", self.cmd_show_hello_hidden, "hidden command", False)

        super(test_module, self).add_command("welcome_msg set", "set welcome message", self.cmd_welcome_set_msg, "welcome_msg set [message]")
        super(test_module, self).add_command("show welcome_msg", "show welcome message", self.cmd_show_welcome_msg)

        super(test_module, self).add_command("show hostname property", "show hostname properties", self.cmd_show_hostname_property)
        super(test_module, self).add_command("show kernel release", "show kernel release", self.cmd_show_kernel_relese)
        super(test_module, self).add_command("show machine id", "show machine id", self.cmd_show_machine_id)

    def cmd_show_hello_world(self):
        print ("hello world")

    def cmd_show_hello_hidden(self):
        print ("hello")

    def cmd_welcome_set_msg(self, args):
        if len(args) != 1:
            raise TypeError

        self.welcome_msg = args[0]

    def cmd_show_welcome_msg(self):
        print (self.welcome_msg)

    def cmd_show_hostname_property(self):
        hostname_dbus = super(test_module, self).get_dbus(HOSTNAME_SERVICE_NAME, HOSTNAME_OBJECT_PATH)
        result = hostname_dbus.dbus_get_property(HOSTNAME_INTERFACE)

        for k,v in result.items():
            print ("%s : %s" % (k, v))

    def cmd_show_kernel_relese(self):
        hostname_dbus = super(test_module, self).get_dbus(HOSTNAME_SERVICE_NAME, HOSTNAME_OBJECT_PATH)
        result = hostname_dbus.dbus_get_property(HOSTNAME_INTERFACE, "KernelRelease")

        print (str(result))

    def cmd_show_machine_id(self):
        hostname_dbus = super(test_module, self).get_dbus(HOSTNAME_SERVICE_NAME, HOSTNAME_OBJECT_PATH)
        result = hostname_dbus.dbus_method_call("GetMachineId", "org.freedesktop.DBus.Peer")

        print (str(result))
