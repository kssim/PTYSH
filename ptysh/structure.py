# -*- coding: utf-8 -*-

"""
Modules related to structure used throughout PTYSH.
"""

import dbus
from collections import OrderedDict

from yaml import Loader
from yaml import MappingNode


class _Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton("Singleton", (object,), {})): pass


class Status(Singleton):

    """
    Class for checking status in PTYSH
    You can check the login(enable) status, the depth of the node, and the name of the node.
    """

    ROOT_DEPTH = 0
    CONFIGURE_DEPTH = 1

    def __init__(self):
        self._login = False
        self._module_depth = self.ROOT_DEPTH
        self._current_node = []
        self._debug = False

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, state):
        self._login = state

    @property
    def module_depth(self):
        return self._module_depth

    def increase_module_depth(self):
        self._module_depth += 1

    def decrease_module_depth(self):
        self._module_depth -= 1

    @property
    def current_node(self):
        return "" if len(self._current_node) == 0 else self._current_node[-1]

    def push_current_node(self, node_name):
        self._current_node.append(node_name)

    def pop_current_node(self):
        self._current_node.pop()

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, state):
        self._debug = state


class PtyshDbus(object):

    """
    The wrapper class of dbus used in PTYSH.
    DBus introspect, property, and method functions are implemented.
    """

    def __init__(self, service_name, object_path):
        """
        Initialize bus and object path.
        """
        self.bus = None
        self.bus_object = None

        try:
            self.bus = dbus.SystemBus()
            self.bus_object = self.bus.get_object(service_name, object_path)
        except Exception as e:
            self.dbus_exception_handler(e)

    def dbus_introspect(self):
        """
        Show introspect information.
        """
        try:
            iface = dbus.Interface(self.bus_object, dbus.INTROSPECTABLE_IFACE)
            result = iface.Introspect()
        except Exception as e:
            self.dbus_exception_handler(e)
        else:
            return result

    def dbus_get_property(self, property_interface, property_name=None):
        """
        Show property information.
        If no property name is given, it shows all available properties.
        """
        try:
            properties = dbus.Interface(self.bus_object, dbus.PROPERTIES_IFACE)

            if property_name:
                result = properties.Get(property_interface, property_name)
            else:
                result = properties.GetAll(property_interface)
        except Exception as e:
            self.dbus_exception_handler(e)
        else:
            return result

    def dbus_method_call(self, method_name, method_interface, *args):
        """
        Show or set the result of method call.
        """
        try:
            method = self.bus_object.get_dbus_method(method_name, method_interface)

            if args:
                result = method(*args)
            else:
                result = method()
        except Exception as e:
            self.dbus_exception_handler(e)
        else:
            return result

    def dbus_exception_handler(self, exception):
        if Status().debug:
            IoControl().print_message(exception)
        else:
            IoControl().print_message("There was a problem sending the dbus message.")
        raise Exception


class OrderedDictYAMLLoader(Loader):

    """
    When loading a YAML file, use OrderDedDictionary to maintain the order of the loaded settings.
    PyYaml does not support OrderedDictionary, so I created a Loader to make OrderdedDictionary available.
    This source code was referenced in the gist below.
      - https://gist.github.com/enaeseth/844388
    """

    def __init__(self, *args, **kwargs):
        Loader.__init__(self, *args, **kwargs)

        self.add_constructor(u"tag:yaml.org,2002:map", type(self).construct_yaml_map)
        self.add_constructor(u"tag:yaml.org,2002:omap", type(self).construct_yaml_map)

    def construct_yaml_map(self, node):
        data = OrderedDict()
        yield data

        value = self.construct_mapping(node)
        if value is not None:
            data.update(value)

    def construct_mapping(self, node, deep=False):
        if not isinstance(node, MappingNode):
            return None

        self.flatten_mapping(node)
        mapping = OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except:
                return None

            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping
