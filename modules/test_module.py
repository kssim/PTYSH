import dbus
from sys import path

from module import PtyshModule

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

        super(test_module, self).add_command("show hello", "show hello", self.cmd_show_hello_hidden, "hidden command", False)

        super(test_module, self).add_command("welcome_msg set", "set welcome message", self.cmd_welcome_set_msg, "welcome_msg set [message]")
        super(test_module, self).add_command("show welcome_msg", "show welcome message", self.cmd_show_welcome_msg)

        super(test_module, self).add_command("show hostname property", "show hostname properties", self.cmd_show_hostname_property)
        super(test_module, self).add_command("show hostname", "show hostname", self.cmd_show_hostname)
        super(test_module, self).add_command("hostname set", "set hostname", self.cmd_hostname_set, "hostname set [hostname]")
        super(test_module, self).add_command("show machine id", "show machine id", self.cmd_show_machine_id)
        super(test_module, self).add_command("show introspect", "show introspect", self.cmd_show_introspect, "", False)

        # get "hostname" dbus interface.
        self.hostname_dbus = super(test_module, self).get_dbus(HOSTNAME_SERVICE_NAME, HOSTNAME_OBJECT_PATH)


    def cmd_show_welcome_msg(self):
        # basic command
        print (self.welcome_msg)

    def cmd_show_hello_hidden(self):
        # hidden command
        print ("hello world")

    def cmd_welcome_set_msg(self, args):
        # basic set command
        if len(args) != 1:
            raise TypeError

        self.welcome_msg = args[0]

    def cmd_show_hostname_property(self):
        # property for get all.
        result = self.hostname_dbus.dbus_get_property(HOSTNAME_INTERFACE)

        for k,v in result.items():
            print ("%s : %s" % (k, v))

    def cmd_show_hostname(self):
        # property for get one item.
        result = self.hostname_dbus.dbus_get_property(HOSTNAME_INTERFACE, "StaticHostname")
        print (str(result))

    def cmd_hostname_set(self, args):
        # method call for SET.
        if len(args) != 1:
            raise TypeError

        result = self.hostname_dbus.dbus_method_call("SetStaticHostname", "org.freedesktop.hostname1", args[0], True)
        print (str(result))

    def cmd_show_machine_id(self):
        # method call for GET.
        result = self.hostname_dbus.dbus_method_call("GetMachineId", dbus.PEER_IFACE)
        print (str(result))

    def cmd_show_introspect(self):
        # Introspect
        result = self.hostname_dbus.dbus_introspect()
        print (str(result))
