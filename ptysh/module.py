# -*- coding: utf-8 -*-

"""
Interface module when developing PTYSH module.
"""

import dbus

from data import Command
from inout import IoControl

class PtyshModule(object):

    """
    Interfaces required when developing a node in a child module
    The child module inherits this interface and implements the node's name, description, and command.
    """

    def __init__(self):
        self._node_name = ""
        self._node_description = ""
        self._command_set = []

        self.dbus_service_name = ""
        self.dbus_object_path = ""
        self.dbus_interface_name = ""

    @property
    def node_name(self):
        return self._node_name

    @property
    def node_description(self):
        return self._node_description

    def init_node(self, node_name, node_description):
        self._node_name = node_name
        self._node_description = node_description

    @property
    def command_set(self):
        return self._command_set

    def add_command(self, command_name, command_desc, command_function, usage="", visible=True, workable=True):
        self._command_set.append(Command(command_name, command_desc, command_function, usage, visible, workable))

    def set_dbus_info(self, service_name, bus_object_path, interface_name):
        if not service_name or not bus_object_path or not interface_name:
            IoControl().print_message("Invalid dbus information")
            return

        self.dbus_service_name = service_name
        self.dbus_object_path = bus_object_path
        self.dbus_interface_name = interface_name

    def dbus_handler(self, data):
        if not self.dbus_service_name or not self.dbus_object_path or not self.dbus_interface_name:
            IoControl().print_message("Invalid dbus information")
            return False

        try:
            bus = dbus.SystemBus()
            bus_object = bus.get_object(self.dbus_service_name, self.dbus_object_path)
            bus_interface = dbus.Interface(bus_object, self.dbus_interface_name)

            bus_interface.receive_signal(data)
        except Exception as e:
            IoControl().print_message("There was a problem sending the dbus message.")
            IoControl().print_message("service name : %s, bus_object_path : %s, interface_name : %s"
                                        % (self.dbus_service_name, self.dbus_object_path, self.dbus_interface_name))
            IoControl().print_message(e)
            raise Exception

        return True
