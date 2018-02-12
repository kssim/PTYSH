# -*- coding: utf-8 -*-

"""
Interface module when developing PTYSH module.
"""

import dbus

from data import Command
from inout import IoControl
from structure import Status

class PtyshModule(object):

    """
    Interfaces required when developing a node in a child module
    The child module inherits this interface and implements the node's name, description, and command.
    """

    def __init__(self):
        self._node_name = ""
        self._node_description = ""
        self._command_set = []

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

    def get_dbus(self, service_name, object_path):
        return PtyshDbus(service_name, object_path)


class PtyshDbus(object):

    def __init__(self, service_name, object_path):
        self.bus = None
        self.bus_object = None

        try:
            self.bus = dbus.SystemBus()
            self.bus_object = self.bus.get_object(service_name, object_path)
        except Exception as e:
            self.dbus_exception_handler(e)

    def dbus_exception_handler(self, exception):
        if Status().debug:
            IoControl().print_message(exception)
        else:
            IoControl().print_message("There was a problem sending the dbus message.")
        raise Exception

    def dbus_get_property(self, property_interface, property_name=None):
        try:
            properties = dbus.Interface(self.bus_object, "org.freedesktop.DBus.Properties")

            if property_name:
                result = properties.Get(property_interface, property_name)
            else:
                result = properties.GetAll(property_interface)
        except Exception as e:
            self.dbus_exception_handler(e)
        else:
            return result

    def dbus_method_call(self, method_name, method_interface, args=None):
        try:
            method = self.bus_object.get_dbus_method(method_name, method_interface)

            if args:
                result = method(args)
            else:
                result = method()
        except Exception as e:
            self.dbus_exception_handler(e)
        else:
            return result
